import numpy as np
import cv2

drawing = False
ix, iy = -1, -1
rect = (0, 0, 1, 1)
mode = 'normal'

img = cv2.imread('image.jpg')
if img is None:
    print("Resim yüklenemedi!")
    exit()

img_orig = img.copy()
img_display = img.copy()

def save_result(image, action_name):
    """İşlenen resmi kaydeder."""
    filename = f"sonuc_{action_name}.jpg"
    cv2.imwrite(filename, image)
    print(f"Kaydedildi: {filename}")


def apply_kmeans(image, k=3):
    """K-means segmentasyonu"""
    data = image.reshape((-1, 3)).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)

    res = center[label.flatten()]
    res = res.reshape((image.shape))

    save_result(res, "kmeans")
    return res

def apply_watershed(image):
    """Watershed segmentasyonu"""

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    ret, sure_fg = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(image, markers)

    boundaries = (markers == -1).astype(np.uint8)
    thick_kernel = np.ones((5, 5), np.uint8)
    dilated_boundaries = cv2.dilate(boundaries, thick_kernel, iterations=1)

    res = image.copy()
    res[dilated_boundaries == 1] = [0, 0, 255]

    save_result(res, "watershed")
    return res


def on_mouse(event, x, y, flags, param):
    """Seçilen dikdörtgenle GrabCut uygulaması"""

    global ix, iy, drawing, rect, img_display, mode, img_orig

    if mode == 'grabcut_selection':
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                img_display = img_orig.copy()
                cv2.rectangle(img_display, (ix, iy), (x, y), (0, 255, 0), 2)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            rect = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))

            mask = np.zeros(img_orig.shape[:2], np.uint8)
            bgd = np.zeros((1, 65), np.float64)
            fgd = np.zeros((1, 65), np.float64)
            cv2.grabCut(img_orig, mask, rect, bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            img_display = img_orig * mask2[:, :, np.newaxis]
            mode = 'normal'
            save_result(img_display, "grabcut")
            print("GrabCut tamamlandı.")


cv2.namedWindow('Segmentasyon Aracı')
cv2.setMouseCallback('Segmentasyon Aracı', on_mouse)

def main():
    global img_display, mode

    print("""
    --- KOMUTLAR ---
    'k' : K-means
    'w' : Watershed
    'g' : GrabCut (Fareyle nesneyi kutu içine al!)
    'r' : Resmi sıfırla
    'q' : Çıkış
    """)

    while True:
        cv2.imshow('Segmentasyon Aracı', img_display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('k'):
            print("K-means uygulanıyor...")
            img_display = apply_kmeans(img_orig)
        elif key == ord('w'):
            print("Watershed uygulanıyor...")
            img_display = apply_watershed(img_orig.copy())
        elif key == ord('g'):
            print("GrabCut Seçimi - Fareyle bir dikdörtgen çiz!")
            mode = 'grabcut_selection'
        elif key == ord('r'):
            img_display = img_orig.copy()
            mode = 'normal'
            print("Resim sıfırlandı.")
        elif key == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
