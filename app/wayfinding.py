"""
길찾기/지도 백엔드 모듈
올림픽공원 지도에서 최단 경로를 찾는 기능 제공
"""
import json
import networkx as nx
import math
import matplotlib
matplotlib.use('Agg')  # GUI 없이 사용하기 위한 설정
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.spatial import KDTree
import numpy as np
from matplotlib import font_manager, rc
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Circle
import platform
import os
from pathlib import Path
import io
import base64
from app.logger import get_logger
from PIL import Image, ImageDraw

logger = get_logger()

# 한글 폰트 설정
def set_korean_font():
    """한글 폰트 설정 (깨짐 방지)"""
    system_name = platform.system()
    if system_name == 'Windows':
        path = "c:/Windows/Fonts/malgun.ttf"
        if os.path.exists(path):
            try:
                font_name = font_manager.FontProperties(fname=path).get_name()
                rc('font', family=font_name)
            except:
                pass
    elif system_name == 'Darwin':  # Mac
        rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False

set_korean_font()

class WayfindingService:
    """길찾기 서비스 클래스"""

    def __init__(self, map_dir='map'):
        """
        초기화
        Args:
            map_dir: 지도 데이터가 있는 디렉토리 경로
        """
        self.map_dir = Path(map_dir)
        self.map_image_path = self.map_dir / '올공맵.png'
        self.roads_geojson_path = self.map_dir / 'roads.geojson'
        self.facilities_json_path = self.map_dir / 'olympic_facilities.json'
        self.mascot_image_path = Path('static/images/mascot_profile.png')

        # 좌표 보정값
        self.CALIB_X_OFFSET = 33.0
        self.CALIB_Y_OFFSET = 33.0
        self.CALIB_X_SCALE = 1.0
        self.CALIB_Y_SCALE = 1.0

        # 거리 환산 (800 픽셀 = 2km)
        self.PIXEL_TO_KM = 2.0 / 800.0  # 1 픽셀 = 0.0025 km

        # 캐시된 데이터
        self._graph = None
        self._facilities = None
        self._tree = None
        self._node_list = None

        logger.info(f"WayfindingService initialized with map_dir: {map_dir}")

    def create_circular_mascot(self, border_color, size=100):
        """원형 액자에 마스코트 이미지를 넣어서 반환"""
        try:
            # 마스코트 이미지 로드
            mascot = Image.open(str(self.mascot_image_path)).convert('RGBA')

            # 정사각형으로 크롭 (중앙 기준)
            width, height = mascot.size
            min_dim = min(width, height)
            left = (width - min_dim) // 2
            top = (height - min_dim) // 2
            mascot = mascot.crop((left, top, left + min_dim, top + min_dim))

            # 리사이즈
            mascot = mascot.resize((size, size), Image.Resampling.LANCZOS)

            # 원형 마스크 생성
            mask = Image.new('L', (size, size), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size, size), fill=255)

            # 마스크 적용
            output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            output.paste(mascot, (0, 0), mask)

            # 테두리가 있는 캔버스 생성
            border_width = 6
            canvas_size = size + border_width * 2
            canvas = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))

            # 흰색 배경 원 그리기
            draw_canvas = ImageDraw.Draw(canvas)
            draw_canvas.ellipse((0, 0, canvas_size, canvas_size), fill='white')

            # 색상 테두리 원 그리기
            draw_canvas.ellipse((0, 0, canvas_size, canvas_size), outline=border_color, width=border_width)

            # 마스코트 이미지를 중앙에 배치
            canvas.paste(output, (border_width, border_width), output)

            return np.array(canvas)

        except Exception as e:
            logger.error(f"Failed to create circular mascot: {e}")
            return None

    def load_graph_data(self):
        """도로망 그래프 및 시설물 데이터 로드 (캐싱)"""
        if self._graph is not None:
            return self._graph, self._facilities, self._tree, self._node_list

        logger.info("Loading graph data...")

        # 1) 시설물 데이터 확인
        if not self.facilities_json_path.exists():
            logger.error(f"Facilities file not found: {self.facilities_json_path}")
            return None, None, None, None

        with open(self.facilities_json_path, 'r', encoding='utf-8') as f:
            self._facilities = json.load(f)

        # 2) 도로망 데이터 확인
        if not self.roads_geojson_path.exists():
            logger.error(f"Roads file not found: {self.roads_geojson_path}")
            return None, None, None, None

        with open(self.roads_geojson_path, 'r', encoding='utf-8') as f:
            geo_data = json.load(f)

        # 3) NetworkX 그래프 생성
        G = nx.Graph()
        for feature in geo_data['features']:
            coords = feature['geometry']['coordinates']

            # 좌표 변환 및 보정
            adjusted_coords = []
            for x, y in coords:
                # Y축 반전 처리 (QGIS 음수 좌표 -> 이미지 양수 좌표)
                if y < 0:
                    y = abs(y)

                # 보정값 적용
                final_x = (x * self.CALIB_X_SCALE) + self.CALIB_X_OFFSET
                final_y = (y * self.CALIB_Y_SCALE) + self.CALIB_Y_OFFSET
                adjusted_coords.append((final_x, final_y))

            # 노드와 엣지(Link) 추가
            for i in range(len(adjusted_coords) - 1):
                u = adjusted_coords[i]
                v = adjusted_coords[i + 1]

                # 가중치(거리) 계산
                dist = math.hypot(u[0] - v[0], u[1] - v[1])

                G.add_edge(u, v, weight=dist)
                G.nodes[u]['pos'] = u
                G.nodes[v]['pos'] = v

        # 4) 빠른 검색을 위한 KDTree 생성
        nodes = list(G.nodes)
        if not nodes:
            logger.error("No nodes found in graph")
            return None, None, None, None

        self._tree = KDTree(np.array(nodes))
        self._node_list = nodes
        self._graph = G

        logger.info(f"Graph loaded: {len(nodes)} nodes, {len(G.edges)} edges")
        return self._graph, self._facilities, self._tree, self._node_list

    def get_facility_names(self):
        """시설물 이름 목록 반환"""
        _, facilities, _, _ = self.load_graph_data()
        if facilities:
            return [f["name"] for f in facilities]
        return []

    def find_path(self, start_name, end_name):
        """
        최단 경로를 찾고 이미지를 생성

        Args:
            start_name: 출발지 이름
            end_name: 도착지 이름

        Returns:
            dict: {
                'success': bool,
                'message': str,
                'image': str (base64 encoded image),
                'distance': float
            }
        """
        try:
            logger.info(f"Finding path from {start_name} to {end_name}")

            # 데이터 로드
            G, facilities, tree, node_list = self.load_graph_data()

            if not G:
                return {
                    'success': False,
                    'message': '지도 데이터 파일이 없거나 로드에 실패했습니다.'
                }

            # 1. 출발지/도착지 좌표 찾기
            start_poi = next((item for item in facilities if item["name"] == start_name), None)
            end_poi = next((item for item in facilities if item["name"] == end_name), None)

            if not start_poi or not end_poi:
                return {
                    'success': False,
                    'message': '선택한 시설물의 위치 정보를 찾을 수 없습니다.'
                }

            start_coords = (start_poi['x'], start_poi['y'])
            end_coords = (end_poi['x'], end_poi['y'])

            # 2. 가장 가까운 도로 노드 매칭 (Snapping)
            _, s_idx = tree.query(start_coords)
            _, e_idx = tree.query(end_coords)
            start_node = node_list[s_idx]
            end_node = node_list[e_idx]

            # 3. 다익스트라(Dijkstra) 경로 탐색
            try:
                path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
                path_length = nx.shortest_path_length(G, source=start_node, target=end_node, weight='weight')
            except nx.NetworkXNoPath:
                return {
                    'success': False,
                    'message': '길이 끊겨 있어 갈 수 없습니다.'
                }

            # 4. 지도 이미지 로드 및 시각화
            if not self.map_image_path.exists():
                return {
                    'success': False,
                    'message': f'지도 이미지 파일이 없습니다: {self.map_image_path}'
                }

            try:
                img = mpimg.imread(str(self.map_image_path))
            except Exception as e:
                logger.error(f"Failed to load map image: {e}")
                return {
                    'success': False,
                    'message': '지도 이미지를 읽을 수 없습니다.'
                }

            # 이미지 크기 설정
            fixed_w = 953
            fixed_h = 676

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(img, extent=[0, fixed_w, fixed_h, 0])

            # 경로 그리기
            path_x = [p[0] for p in path]
            path_y = [p[1] for p in path]

            ax.plot(path_x, path_y, color='red', linewidth=2, label='추천 경로', alpha=0.5)

            # 출발지/도착지 표시 (원형 액자 마스코트)
            if self.mascot_image_path.exists():
                # 출발지 원형 마스코트 (파란색 테두리)
                start_mascot = self.create_circular_mascot('#3399ff', size=50)
                if start_mascot is not None:
                    imagebox_start = OffsetImage(start_mascot, zoom=0.5)
                    ab_start = AnnotationBbox(imagebox_start, start_coords, frameon=False,
                                              box_alignment=(0.5, 0.5))
                    ax.add_artist(ab_start)
                else:
                    ax.scatter(*start_coords, color='#3399ff', s=250, zorder=5, edgecolors='white', linewidth=3, alpha=0.9)

                # 도착지 원형 마스코트 (초록색 테두리)
                end_mascot = self.create_circular_mascot('#33ff99', size=50)
                if end_mascot is not None:
                    imagebox_end = OffsetImage(end_mascot, zoom=0.5)
                    ab_end = AnnotationBbox(imagebox_end, end_coords, frameon=False,
                                           box_alignment=(0.5, 0.5))
                    ax.add_artist(ab_end)
                else:
                    ax.scatter(*end_coords, color='#33ff99', s=250, zorder=5, edgecolors='white', linewidth=3, alpha=0.9)
            else:
                # 마스코트 파일이 없으면 원으로 표시
                ax.scatter(*start_coords, color='#3399ff', s=250, zorder=5, edgecolors='white', linewidth=3, alpha=0.9)
                ax.scatter(*end_coords, color='#33ff99', s=250, zorder=5, edgecolors='white', linewidth=3, alpha=0.9)

            # 꾸미기
            ax.axis('off')

            # 이미지를 base64로 인코딩
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)

            # 거리를 km로 환산
            distance_km = path_length * self.PIXEL_TO_KM

            logger.info(f"Path found successfully: distance={path_length:.2f} pixels ({distance_km:.2f} km)")

            return {
                'success': True,
                'message': f'{start_name}에서 {end_name}까지의 최단 경로입니다!',
                'image': image_base64,
                'distance': float(distance_km),
                'distance_pixels': float(path_length),
                'start': start_name,
                'end': end_name
            }

        except Exception as e:
            logger.error(f"Error in find_path: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'경로 찾기 중 오류가 발생했습니다: {str(e)}'
            }

    def get_nearest_facility(self, x, y, max_distance=50):
        """
        주어진 좌표에서 가장 가까운 시설물 찾기

        Args:
            x: X 좌표
            y: Y 좌표
            max_distance: 최대 거리 (픽셀)

        Returns:
            str: 시설물 이름 또는 None
        """
        _, facilities, _, _ = self.load_graph_data()

        if not facilities:
            return None

        min_dist = float('inf')
        nearest = None

        for facility in facilities:
            fx, fy = facility['x'], facility['y']
            dist = math.hypot(x - fx, y - fy)

            if dist < min_dist and dist <= max_distance:
                min_dist = dist
                nearest = facility['name']

        return nearest

    def find_path_from_coords(self, start_x, start_y, end_x, end_y):
        """
        좌표를 이용한 경로 찾기 (지도 클릭 기반)

        Args:
            start_x, start_y: 출발지 좌표
            end_x, end_y: 도착지 좌표

        Returns:
            dict: 경로 찾기 결과
        """
        try:
            logger.info(f"Finding path from coords ({start_x}, {start_y}) to ({end_x}, {end_y})")

            # 데이터 로드
            G, facilities, tree, node_list = self.load_graph_data()

            if not G:
                return {
                    'success': False,
                    'message': '지도 데이터 파일이 없거나 로드에 실패했습니다.'
                }

            # 1. 클릭한 좌표에서 가장 가까운 도로 노드 찾기
            start_coords = (start_x, start_y)
            end_coords = (end_x, end_y)

            _, s_idx = tree.query(start_coords)
            _, e_idx = tree.query(end_coords)
            start_node = node_list[s_idx]
            end_node = node_list[e_idx]

            # 2. 다익스트라 경로 탐색
            try:
                path = nx.shortest_path(G, source=start_node, target=end_node, weight='weight')
                path_length = nx.shortest_path_length(G, source=start_node, target=end_node, weight='weight')
            except nx.NetworkXNoPath:
                return {
                    'success': False,
                    'message': '길이 끊겨 있어 갈 수 없습니다.'
                }

            # 3. 지도 이미지 로드 및 시각화
            if not self.map_image_path.exists():
                return {
                    'success': False,
                    'message': f'지도 이미지 파일이 없습니다: {self.map_image_path}'
                }

            try:
                img = mpimg.imread(str(self.map_image_path))
            except Exception as e:
                logger.error(f"Failed to load map image: {e}")
                return {
                    'success': False,
                    'message': '지도 이미지를 읽을 수 없습니다.'
                }

            # 이미지 크기 설정
            fixed_w = 953
            fixed_h = 676

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.imshow(img, extent=[0, fixed_w, fixed_h, 0])

            # 경로 그리기
            path_x = [p[0] for p in path]
            path_y = [p[1] for p in path]

            ax.plot(path_x, path_y, color='red', linewidth=3, label='추천 경로', alpha=0.7)

            # 출발지/도착지 표시 (원형 액자 마스코트)
            if self.mascot_image_path.exists():
                # 출발지 원형 마스코트 (파란색 테두리)
                start_mascot = self.create_circular_mascot('#3399ff', size=50)
                if start_mascot is not None:
                    imagebox_start = OffsetImage(start_mascot, zoom=0.5)
                    ab_start = AnnotationBbox(imagebox_start, (start_x, start_y), frameon=False,
                                              box_alignment=(0.5, 0.5))
                    ax.add_artist(ab_start)
                else:
                    ax.scatter(start_x, start_y, color='#3399ff', s=250, zorder=5, edgecolors='white', linewidth=3, alpha=0.9)

                # 도착지 원형 마스코트 (초록색 테두리)
                end_mascot = self.create_circular_mascot('#33ff99', size=50)
                if end_mascot is not None:
                    imagebox_end = OffsetImage(end_mascot, zoom=0.5)
                    ab_end = AnnotationBbox(imagebox_end, (end_x, end_y), frameon=False,
                                           box_alignment=(0.5, 0.5))
                    ax.add_artist(ab_end)
                else:
                    ax.scatter(end_x, end_y, color='#33ff99', s=250, zorder=5, edgecolors='white', linewidth=3, alpha=0.9)
            else:
                # 마스코트 파일이 없으면 원으로 표시
                ax.scatter(start_x, start_y, color='#3399ff', s=250, zorder=5, edgecolors='white', linewidth=3, alpha=0.9)
                ax.scatter(end_x, end_y, color='#33ff99', s=250, zorder=5, edgecolors='white', linewidth=3, alpha=0.9)

            # 꾸미기
            ax.axis('off')

            # 이미지를 base64로 인코딩
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=150)
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)

            # 거리를 km로 환산
            distance_km = path_length * self.PIXEL_TO_KM

            logger.info(f"Path found successfully: distance={path_length:.2f} pixels ({distance_km:.2f} km)")

            return {
                'success': True,
                'message': '최단 경로를 찾았습니다!',
                'image': image_base64,
                'distance': float(distance_km),
                'distance_pixels': float(path_length),
                'start_coords': {'x': start_x, 'y': start_y},
                'end_coords': {'x': end_x, 'y': end_y}
            }

        except Exception as e:
            logger.error(f"Error in find_path_from_coords: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'경로 찾기 중 오류가 발생했습니다: {str(e)}'
            }

    def find_nearest_facility_by_category(self, x, y, category='toilet', name_pattern=None):
        """
        특정 카테고리 또는 이름 패턴의 가장 가까운 시설물 찾기 및 경로 표시

        Args:
            x, y: 현재 위치 좌표
            category: 시설물 카테고리 (예: 'toilet')
            name_pattern: 시설물 이름 검색 패턴 (예: '매점', '음수대')

        Returns:
            dict: 경로 찾기 결과
        """
        try:
            logger.info(f"Finding nearest facility - category: {category}, pattern: {name_pattern} from ({x}, {y})")

            # 데이터 로드
            G, facilities, tree, node_list = self.load_graph_data()

            if not G or not facilities:
                return {
                    'success': False,
                    'message': '지도 데이터 파일이 없거나 로드에 실패했습니다.'
                }

            # 1. 카테고리 또는 이름 패턴으로 시설물 필터링
            if name_pattern:
                # 이름 패턴으로 검색
                category_facilities = [f for f in facilities if name_pattern in f.get('name', '')]
            else:
                # 카테고리로 검색
                category_facilities = [f for f in facilities if f.get('category') == category]

            if not category_facilities:
                search_term = name_pattern if name_pattern else category
                return {
                    'success': False,
                    'message': f'{search_term} 시설물을 찾을 수 없습니다.'
                }

            # 2. 가장 가까운 시설물 찾기
            min_dist = float('inf')
            nearest_facility = None

            for facility in category_facilities:
                fx, fy = facility['x'], facility['y']
                dist = math.hypot(x - fx, y - fy)

                if dist < min_dist:
                    min_dist = dist
                    nearest_facility = facility

            if not nearest_facility:
                return {
                    'success': False,
                    'message': '가까운 시설물을 찾을 수 없습니다.'
                }

            # 3. 경로 찾기 (좌표 기반)
            return self.find_path_from_coords(
                x, y,
                nearest_facility['x'], nearest_facility['y']
            )

        except Exception as e:
            logger.error(f"Error in find_nearest_facility_by_category: {e}", exc_info=True)
            return {
                'success': False,
                'message': f'시설물 찾기 중 오류가 발생했습니다: {str(e)}'
            }
