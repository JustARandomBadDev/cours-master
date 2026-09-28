from typing import Tuple, Optional
import math

import cv2
import numpy as np


cap = cv2.VideoCapture(0)

reference_image = cv2.imread("small_flyer.jpeg")
target_image = cv2.imread("meme.png")
target_image = cv2.flip(target_image, 1)


method = "SIFT"

if method == "SIFT":
    keypoints_detector = cv2.SIFT_create()

    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    matcher = cv2.FlannBasedMatcher(index_params, search_params)

    matches_thresh = 30
else:
    keypoints_detector = cv2.ORB_create(nfeatures=1000)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    matches_thresh = 10

kp1, des1 = keypoints_detector.detectAndCompute(reference_image, None)

ok = True
while ok:
    ok, camera_frame = cap.read()
    if not ok:
        print("Error: Could not open video.")
        exit()
    
    camera_frame = cv2.resize(camera_frame, (853, 480))

    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("q pressed, closing.")
        break

    kp2, des2 = keypoints_detector.detectAndCompute(camera_frame, None)

    matches = matcher.knnMatch(des1, des2, k=2)

    # quality filter
    good_matches = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good_matches.append(m)
    matches = good_matches
    print(f"Found {len(matches)} good matches")

   # display matches
    display_image = camera_frame.copy()
    display_image = cv2.drawMatchesKnn(reference_image, kp1, camera_frame, kp2, [matches], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv2.imshow("Keypoints", display_image)

    # homography
    if len(matches) > matches_thresh:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0, maxIters=2000, confidence=0.999)
        matchesMask = mask.ravel().tolist()

        h,w, _ = reference_image.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)

        camera_frame = cv2.polylines(camera_frame,[np.int32(dst)],True,(255,0,0),3, cv2.LINE_AA)

        # warp target image
        hT, wT, cT = target_image.shape
        pts2 = np.float32([ [0,0],[0,hT-1],[wT-1,hT-1],[wT-1,0] ]).reshape(-1,1,2)
        M2 = cv2.getPerspectiveTransform(pts2,dst)
        warped_target = cv2.warpPerspective(target_image,M2,(camera_frame.shape[1], camera_frame.shape[0]))

        # create mask
        mask_new = np.zeros((camera_frame.shape[0], camera_frame.shape[1]), dtype=np.uint8)
        cv2.fillPoly(mask_new, [np.int32(dst)], (255, 255, 255))
        mask_inv = cv2.bitwise_not(mask_new)

        # black-out the area of the flyer in the camera frame
        img1_bg = cv2.bitwise_and(camera_frame, camera_frame, mask=mask_inv)

        # take only region of flyer from warped flyer image.
        img2_fg = cv2.bitwise_and(warped_target, warped_target, mask=mask_new)

        # put together
        camera_frame = cv2.add(img1_bg, img2_fg)

    camera_frame = cv2.flip(camera_frame, 1)
    cv2.imshow("Augmented Reality Flyer", camera_frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("q pressed, closing.")
        break