import json
import networkx as nx
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.spatial import KDTree
import numpy as np
from matplotlib import font_manager, rc

path = "c:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=path).get_name()
rc('font', family=font_name)

plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 설정 (파일 경로 및 이미지 크기)
# ==========================================
MAP_IMAGE_PATH = '올공맵.png'  # 배경 지도 이미지 (아까 자른거)
ROADS_GEOJSON_PATH = 'roads.geojson'  # QGIS에서 만든 도로망
FACILITIES_JSON_PATH = 'olympic_facilities.json'  # 크롤링한 시설물 데이터

# 지도 전체 높이 (Y축 반전 계산용, 아까 SVG Height 값)
MAP_HEIGHT = 676.87

CALIB_X_OFFSET = 33.0   # 오른쪽(+)이나 왼쪽(-)으로 이동 (픽셀 단위)
CALIB_Y_OFFSET = 33.0  # 아래(+)나 위(-)로 이동
CALIB_X_SCALE  = 1.0  # 가로로 늘리기(1.0보다 큼) / 줄이기(1.0보다 작음)
CALIB_Y_SCALE  = 1.0    # 세로로 늘리기 / 줄이기


# ==========================================
# 2. 그래프 구축 함수 (보정 로직 적용)
# ==========================================
def create_graph_from_geojson(geojson_file):
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    G = nx.Graph()

    for feature in data['features']:
        coords = feature['geometry']['coordinates']

        adjusted_coords = []
        for x, y in coords:
            # 1. Y축 반전 (음수 -> 양수)
            if y < 0: y = abs(y)

            # 2. [핵심] 보정값 적용 (스케일링 후 이동)
            final_x = (x * CALIB_X_SCALE) + CALIB_X_OFFSET
            final_y = (y * CALIB_Y_SCALE) + CALIB_Y_OFFSET

            adjusted_coords.append((final_x, final_y))

        for i in range(len(adjusted_coords) - 1):
            u = adjusted_coords[i]
            v = adjusted_coords[i + 1]
            dist = math.hypot(u[0] - v[0], u[1] - v[1])
            G.add_edge(u, v, weight=dist)
            G.nodes[u]['pos'] = u
            G.nodes[v]['pos'] = v

    return G

# ==========================================
# 3. 스내핑 함수 (시설물 -> 가장 가까운 도로 찾기)
# ==========================================
def get_nearest_node(G, point):
    # 그래프의 모든 노드 좌표 추출
    nodes = list(G.nodes)
    node_coords = np.array(nodes)

    # KDTree로 가장 가까운 이웃 검색 (속도 빠름)
    tree = KDTree(node_coords)
    dist, idx = tree.query(point)

    return nodes[idx]  # 가장 가까운 노드 좌표 반환


# ==========================================
# 4. 클릭 이벤트 핸들러 클래스
# ==========================================
class InteractivePathFinder:
    def __init__(self, graph, img_path, facilities):
        self.G = graph
        self.img = mpimg.imread(img_path)
        self.facilities = facilities

        # 상태 변수
        self.start_point = None
        self.end_point = None
        self.path = None
        self.path_line = None
        self.markers = []

        # 도착지 설정 (기본값 - 나중에 변경 가능)
        self.end_point = (450, 400)  # 기본 도착지

    def onclick(self, event):
        """마우스 클릭 이벤트 처리"""
        if event.inaxes is None:
            return

        # 클릭한 위치 좌표
        click_x, click_y = event.xdata, event.ydata

        if event.button == 1:  # 왼쪽 클릭 = 출발지 설정
            self.start_point = (click_x, click_y)
            print(f"출발지 설정: ({click_x:.1f}, {click_y:.1f})")
            self.update_path()

        elif event.button == 3:  # 오른쪽 클릭 = 도착지 설정
            self.end_point = (click_x, click_y)
            print(f"도착지 설정: ({click_x:.1f}, {click_y:.1f})")
            self.update_path()

    def update_path(self):
        """경로 재계산 및 화면 업데이트"""
        if self.start_point is None or self.end_point is None:
            print("출발지와 도착지를 모두 설정해주세요.")
            return

        # 기존 마커와 경로 제거
        for marker in self.markers:
            marker.remove()
        self.markers = []

        if self.path_line is not None:
            self.path_line.remove()
            self.path_line = None

        # 가장 가까운 도로 노드 찾기
        start_node = get_nearest_node(self.G, self.start_point)
        end_node = get_nearest_node(self.G, self.end_point)

        # 경로 계산
        try:
            self.path = nx.shortest_path(self.G, source=start_node, target=end_node, weight='weight')
            print(f"경로 찾기 성공! (노드 {len(self.path)}개)")

            # 경로 그리기
            path_x = [p[0] for p in self.path]
            path_y = [p[1] for p in self.path]
            self.path_line, = self.ax.plot(path_x, path_y, color='red', linewidth=3,
                                           marker='o', markersize=3, label='추천 경로', zorder=10)

        except nx.NetworkXNoPath:
            print("경로를 찾을 수 없습니다. (길이 끊겨 있습니다!)")
            self.path = None

        # 출발지/도착지 마커 표시
        start_marker = self.ax.scatter(*self.start_point, color='blue', s=150,
                                       label='출발지 (클릭)', zorder=15, edgecolors='white', linewidths=2)
        end_marker = self.ax.scatter(*self.end_point, color='green', s=150,
                                     label='도착지', zorder=15, edgecolors='white', linewidths=2)

        # 스냅된 노드 표시
        snap_start = self.ax.scatter(*start_node, color='cyan', s=50, marker='x',
                                     label='매칭된 출발 노드', zorder=12)
        snap_end = self.ax.scatter(*end_node, color='yellow', s=50, marker='x',
                                   label='매칭된 도착 노드', zorder=12)

        self.markers = [start_marker, end_marker, snap_start, snap_end]

        # 범례 업데이트
        self.ax.legend(loc='upper right')
        plt.draw()

    def start(self):
        """인터랙티브 모드 시작"""
        self.fig, self.ax = plt.subplots(figsize=(14, 9))

        # 배경 지도 그리기
        self.ax.imshow(self.img, extent=[0, 953, 676, 0])

        # 전체 도로망 그리기 (회색 얇은 선)
        for u, v in self.G.edges():
            x_vals = [u[0], v[0]]
            y_vals = [u[1], v[1]]
            self.ax.plot(x_vals, y_vals, color='gray', linewidth=0.5, alpha=0.4)

        # 클릭 이벤트 연결
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        plt.title("지도를 클릭하세요\n[왼쪽 클릭: 출발지 설정 | 오른쪽 클릭: 도착지 설정]",
                 fontsize=14, fontweight='bold')
        plt.legend()
        plt.tight_layout()
        plt.show()


# ==========================================
# 5. 실행 로직
# ==========================================

# 1) 데이터 로드
print("1. 도로망 구축 중...")
G = create_graph_from_geojson(ROADS_GEOJSON_PATH)
print(f"   -> 노드 {len(G.nodes)}개, 링크 {len(G.edges)}개 생성 완료!")

# 2) 시설물 DB 로드
with open(FACILITIES_JSON_PATH, 'r', encoding='utf-8') as f:
    facilities = json.load(f)

# 3) 인터랙티브 경로 찾기 시작
print("\n인터랙티브 지도를 시작합니다...")
print("- 왼쪽 클릭: 출발지(현재 위치) 설정")
print("- 오른쪽 클릭: 도착지 설정")

finder = InteractivePathFinder(G, MAP_IMAGE_PATH, facilities)
finder.start()