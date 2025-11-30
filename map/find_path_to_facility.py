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
# 1. 설정
# ==========================================
MAP_IMAGE_PATH = 'map/올공맵.png'
ROADS_GEOJSON_PATH = 'map/roads.geojson'
FACILITIES_JSON_PATH = 'map/olympic_facilities.json'

MAP_HEIGHT = 676.87
CALIB_X_OFFSET = 33.0
CALIB_Y_OFFSET = 33.0
CALIB_X_SCALE  = 1.0
CALIB_Y_SCALE  = 1.0


# ==========================================
# 2. 그래프 구축
# ==========================================
def create_graph_from_geojson(geojson_file):
    with open(geojson_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    G = nx.Graph()

    for feature in data['features']:
        coords = feature['geometry']['coordinates']

        adjusted_coords = []
        for x, y in coords:
            if y < 0: y = abs(y)
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
# 3. 스내핑
# ==========================================
def get_nearest_node(G, point):
    nodes = list(G.nodes)
    node_coords = np.array(nodes)
    tree = KDTree(node_coords)
    dist, idx = tree.query(point)
    return nodes[idx]


# ==========================================
# 4. 특정 시설물로 가는 인터랙티브 경로 찾기
# ==========================================
class FacilityNavigator:
    def __init__(self, graph, img_path, facilities, destination_name):
        self.G = graph
        self.img = mpimg.imread(img_path)
        self.facilities = facilities
        self.destination_name = destination_name

        # 도착지 시설물 찾기
        dest_facility = next((f for f in facilities if f["name"] == destination_name), None)
        if dest_facility is None:
            print(f"경고: '{destination_name}' 시설물을 찾을 수 없습니다!")
            self.destination = (450, 400)  # 기본값
        else:
            self.destination = (dest_facility['x'], dest_facility['y'])
            print(f"도착지 설정: {destination_name} ({self.destination})")

        self.start_point = None
        self.path = None
        self.path_line = None
        self.markers = []

    def onclick(self, event):
        """왼쪽 클릭 시 출발지 설정 및 경로 계산"""
        if event.inaxes is None or event.button != 1:
            return

        # 클릭한 위치 = 현재 위치
        click_x, click_y = event.xdata, event.ydata
        self.start_point = (click_x, click_y)
        print(f"\n현재 위치 클릭: ({click_x:.1f}, {click_y:.1f})")
        self.update_path()

    def update_path(self):
        """경로 재계산 및 화면 업데이트"""
        if self.start_point is None:
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
        end_node = get_nearest_node(self.G, self.destination)

        print(f"가장 가까운 출발 노드: {start_node}")
        print(f"도착지 노드: {end_node}")

        # 경로 계산
        try:
            self.path = nx.shortest_path(self.G, source=start_node, target=end_node, weight='weight')

            # 경로 길이 계산
            path_length = sum(
                math.hypot(self.path[i][0] - self.path[i+1][0],
                          self.path[i][1] - self.path[i+1][1])
                for i in range(len(self.path) - 1)
            )

            print(f"✓ 경로 찾기 성공! (총 {len(self.path)}개 노드, 약 {path_length:.1f}픽셀)")

            # 경로 그리기
            path_x = [p[0] for p in self.path]
            path_y = [p[1] for p in self.path]
            self.path_line, = self.ax.plot(path_x, path_y, color='#FF4444', linewidth=4,
                                           marker='o', markersize=4, label='추천 경로',
                                           zorder=10, alpha=0.8)

        except nx.NetworkXNoPath:
            print("✗ 경로를 찾을 수 없습니다. (도로가 연결되지 않았습니다!)")
            self.path = None

        # 출발지/도착지 마커 표시
        start_marker = self.ax.scatter(*self.start_point, color='blue', s=200,
                                       label='현재 위치', zorder=15,
                                       edgecolors='white', linewidths=3, marker='o')
        end_marker = self.ax.scatter(*self.destination, color='green', s=200,
                                     label=f'도착지: {self.destination_name}', zorder=15,
                                     edgecolors='white', linewidths=3, marker='s')

        # 스냅된 노드 표시
        snap_start = self.ax.scatter(*start_node, color='cyan', s=60, marker='x',
                                     linewidths=3, label='출발 노드', zorder=12)

        self.markers = [start_marker, end_marker, snap_start]

        # 범례 업데이트
        self.ax.legend(loc='upper right', fontsize=10)
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
            self.ax.plot(x_vals, y_vals, color='gray', linewidth=0.5, alpha=0.3)

        # 목적지 미리 표시
        self.ax.scatter(*self.destination, color='green', s=200,
                       label=f'도착지: {self.destination_name}', zorder=15,
                       edgecolors='white', linewidths=3, marker='s')

        # 클릭 이벤트 연결
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        plt.title(f"현재 위치를 클릭하면 '{self.destination_name}'까지 경로를 안내합니다",
                 fontsize=14, fontweight='bold', pad=20)
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()


# ==========================================
# 5. 실행
# ==========================================
if __name__ == "__main__":
    print("=" * 50)
    print("특정 시설물로 가는 경로 안내 시스템")
    print("=" * 50)

    # 1) 데이터 로드
    print("\n1. 도로망 구축 중...")
    G = create_graph_from_geojson(ROADS_GEOJSON_PATH)
    print(f"   ✓ 노드 {len(G.nodes)}개, 링크 {len(G.edges)}개 생성 완료!")

    # 2) 시설물 DB 로드
    with open(FACILITIES_JSON_PATH, 'r', encoding='utf-8') as f:
        facilities = json.load(f)
    print(f"   ✓ 시설물 {len(facilities)}개 로드 완료!")

    # 3) 도착지 설정 (여기를 변경하세요!)
    DESTINATION = "화장실1"  # 원하는 시설물 이름으로 변경

    # 사용 가능한 시설물 목록 표시
    print(f"\n사용 가능한 시설물 목록 (일부):")
    for i, fac in enumerate(facilities[:10]):
        print(f"   - {fac['name']}")
    if len(facilities) > 10:
        print(f"   ... 외 {len(facilities) - 10}개")

    # 4) 네비게이터 시작
    print(f"\n목적지: {DESTINATION}")
    print("지도에서 현재 위치를 클릭하세요!\n")

    navigator = FacilityNavigator(G, MAP_IMAGE_PATH, facilities, DESTINATION)
    navigator.start()
