"""モジュールのインポート"""
import numpy as np
from sklearn.cluster import KMeans
import pickle
from src.visualize_data import (
    show_signals, show_spectrums, show_all_spectrums, show_sses,
    show_fft_clusters, show_fft_centers, show_signals_with_cluster
)   # 自作モジュール

"""データの読み込み"""
n_data = 50         # データ数
n_samples = 256     # 1データに含まれる点の数
t = np.zeros((n_data, n_samples))   # 時刻
x = np.zeros((n_data, n_samples))   # 信号強度
for i in range(n_data):
    data = np.loadtxt(f"./data/example2/{i:04}.csv", delimiter=",")
    t[i, :] = data[:, 0]    # 1列目が時刻のデータ
    x[i, :] = data[:, 1]    # 2列目が信号強度のデータ

show_signals(t, x)  # 読み込んだデータのグラフ表示

"""FFT"""
df = 1 / (t[0, -1] - t[0, 0])       # 周波数の刻み幅
f = np.arange(n_samples // 2) * df  # 周波数領域
feats = np.zeros((n_data, n_samples // 2))   # 特徴量を格納する配列
for i in range(len(x)):
    fourier = np.fft.fft(x[i, :])
    spectrum = np.sqrt(fourier.real**2 + fourier.imag**2)   # パワースペクトルの算出
    spectrum = spectrum[: n_samples // 2]
    feats[i, :] = spectrum

show_spectrums(f, feats)        # パワースペクトルを2次元グラフで一部表示
show_all_spectrums(f, feats)    # パワースペクトルを3次元グラフで全て表示

"""エルボー法"""
sses = np.zeros(10)     # SSEの値を格納する配列
for n_clusters in range(1, 11):
    kmeans = KMeans(n_clusters, random_state=100).fit(feats)    # k-meansモデルの学習
    sses[n_clusters - 1] = kmeans.inertia_   # 誤差平方和（SSE）
show_sses(sses)     # クラスタ数に応じるSSEの確認

"""k-meansの実行"""
n_clusters = 3

kmeans = KMeans(n_clusters, random_state=100).fit(feats)    # 学習
centers = kmeans.cluster_centers_   # クラスタ中心
labels = kmeans.labels_             # 各データが属するクラスタ

show_fft_clusters(f, feats, labels)         # クラスタリング結果のグラフ
show_fft_centers(f, centers)                # クラスタ中心のグラフ
show_signals_with_cluster(t, x, labels)     # 波形をクラスタで色分け表示

with open("kmeans_model_2.pkl", "wb") as fp:
    pickle.dump(kmeans, fp)     # モデル保存
