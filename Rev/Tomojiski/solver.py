## Author : IronByte
## Securinets Quals 2023

def solve():
    v = [3, 4, 5, 6, 6, 6, 12, 13, 17, 9, 9, 9, 9, 14, 32, 33, 34, 20, 20, 21, 21, 23, 46, 47, 49, 55, 56, 30, 59, 60, 62, 63, 32, 32, 32, 67, 75, 42, 47, 86, 47, 47, 90, 93, 50, 95, 52, 53, 101, 53, 103, 104, 105, 106, 107, 53, 54, 55, 113, 55, 56, 118, 57, 57, 57, 57, 57, 57, 127, 133, 137, 140, 142, 143, 148, 75, 151, 152, 155, 79, 163, 167, 168, 169, 173, 89, 90, 90, 91, 180, 91, 184, 185, 99, 100, 100, 197, 199, 102, 201, 102, 102, 102, 103, 103, 103, 104, 105, 105, 217, 108, 219, 108, 109, 109, 226, 114, 231, 114, 115, 116, 116, 116, 116, 117, 247, 249, 126, 254, 256, 259, 262, 263, 132, 266, 267, 270, 137, 277, 279, 140, 281, 141, 143, 289, 290, 291, 292, 147, 297, 148, 157, 158, 311, 313, 160, 317, 318, 162, 321, 322, 324, 325, 164, 330, 338, 340, 175, 178, 179, 351, 353, 357, 185, 185, 361, 186, 186, 364, 187, 188, 188, 371, 372, 190, 190, 376, 377, 382, 384, 385, 387, 197, 391, 198, 200, 396, 201, 399, 201, 201, 201, 203, 206, 213, 421, 217, 220, 221, 431, 223, 435, 224, 224, 438, 440, 443, 228, 228, 230, 231, 453, 232, 232, 456, 457, 233, 461, 462, 463, 234, 234, 237, 473, 240, 479, 245, 245, 246, 250, 490, 251, 493, 497, 498, 499, 500, 254, 502, 254, 504, 505, 508, 256, 256, 511, 256, 515, 516, 259, 522, 523, 263, 263, 528, 264, 264, 265, 533, 534, 267, 538, 539, 541, 268, 543, 544, 268, 547, 270, 277, 277, 561, 279, 566, 568, 284, 572, 573, 285, 285, 285, 288, 582, 583, 289, 586, 291, 291, 591, 594, 596, 597, 598, 600, 602, 603, 604, 297, 607, 307, 307, 621, 317, 632, 320, 638, 322, 324, 643, 325, 325, 325, 649, 326, 326, 652, 326, 656, 657, 329, 661, 664, 667, 672, 673, 674, 675, 342, 681, 344, 685, 344, 687, 688, 690, 345, 692, 345, 695, 697, 347, 700, 348, 702, 703, 705, 350, 350, 350, 712, 352, 352, 353, 353, 718, 354, 725, 361, 362, 733, 365, 368, 743, 370, 370, 372, 373, 751, 752, 753, 754, 374, 757, 375, 375, 761, 375, 767, 380, 771, 381, 381, 774, 779, 393, 393, 790, 398, 400, 400, 403, 403, 809, 810, 413, 823, 827, 829, 421, 831, 833, 837, 839, 842, 843, 844, 434, 853, 855, 857, 437, 861, 439, 863, 864, 865, 444, 873, 449, 882, 452, 884, 452, 887, 455, 461, 461, 463, 904, 465, 907, 908, 467, 911, 468, 469, 916, 917, 469, 920, 470, 922, 471, 471, 471, 471, 471, 929, 472, 934, 474, 475, 476, 476, 478, 944, 946, 949, 481, 952, 959, 962, 491, 495, 970, 971, 973, 979, 502, 982, 502, 502, 987, 505, 992, 993, 994, 997, 509, 509, 1003, 512, 512, 1006, 1008, 1011, 519, 520, 522, 522, 523, 522, 521, 520, 519, 1024, 1024, 516, 515, 514, 513, 512, 1024, 1024, 509, 508, 1024, 506, 1024, 1024, 1024, 502, 501, 1024, 499, 498, 1024, 496, 495, 494, 1024, 492, 491, 490, 1024, 1024, 487, 486, 485, 1024, 483, 482, 481, 480, 479, 1024, 477, 1024, 475, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 467, 466, 1024, 1024, 463, 462, 1024, 1024, 1024, 458, 1024, 456, 1024, 454, 1024, 452, 451, 450, 449, 448, 1024, 1024, 1024, 444, 1024, 442, 441, 440, 1024, 438, 1024, 436, 435, 1024, 433, 1024, 1024, 430, 1024, 428, 427, 426, 1024, 424, 1024, 422, 421, 420, 419, 1024, 417, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 407, 406, 1024, 1024, 403, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 394, 1024, 392, 1024, 1024, 389, 1024, 1024, 386, 385, 1024, 1024, 382, 381, 1024, 379, 378, 377, 1024, 375, 374, 373, 372, 371, 1024, 1024, 368, 367, 1024, 365, 1024, 363, 1024, 1024, 360, 1024, 1024, 357, 1024, 1024, 1024, 1024, 352, 351, 350, 349, 1024, 1024, 1024, 1024, 344, 343, 1024, 1024, 340, 339, 338, 337, 336, 1024, 334, 333, 332, 331, 1024, 329, 1024, 327, 326, 1024, 324, 323, 322, 321, 1024, 319, 1024, 317, 316, 315, 1024, 1024, 312, 311, 310, 1024, 308, 307, 306, 1024, 304, 1024, 1024, 1024, 1024, 299, 1024, 1024, 1024, 295, 1024, 293, 1024, 291, 1024, 1024, 288, 1024, 1024, 1024, 284, 1024, 1024, 281, 280, 279, 1024, 1024, 276, 1024, 274, 273, 272, 271, 270, 1024, 268, 267, 1024, 265, 264, 263, 262, 1024, 1024, 1024, 1024, 257, 1024, 255, 1024, 253, 252, 251, 250, 1024, 1024, 1024, 1024, 245, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 236, 235, 234, 1024, 1024, 1024, 1024, 1024, 228, 1024, 1024, 225, 224, 1024, 1024, 1024, 220, 219, 1024, 1024, 1024, 215, 214, 1024, 1024, 1024, 1024, 1024, 1024, 1024, 206, 1024, 1024, 1024, 1024, 201, 1024, 1024, 1024, 197, 1024, 195, 194, 193, 1024, 191, 1024, 1024, 1024, 187, 1024, 185, 1024, 1024, 182, 181, 180, 1024, 1024, 1024, 1024, 1024, 1024, 173, 1024, 171, 1024, 169, 1024, 167, 166, 1024, 1024, 163, 162, 161, 160, 159, 1024, 1024, 1024, 1024, 1024, 153, 1024, 151, 1024, 1024, 1024, 1024, 146, 1024, 1024, 1024, 142, 141, 140, 139, 1024, 137, 1024, 1024, 134, 1024, 1024, 1024, 1024, 1024, 1024, 127, 126, 1024, 1024, 123, 1024, 1024, 120, 119, 1024, 117, 116, 1024, 114, 113, 1024, 111, 1024, 109, 108, 107, 106, 1024, 104, 103, 102, 1024, 100, 99, 98, 97, 96, 95, 1024, 93, 1024, 1024, 90, 89, 1024, 87, 1024, 85, 84, 1024, 1024, 81, 80, 1024, 78, 1024, 1024, 75, 74, 1024, 72, 1024, 1024, 1024, 1024, 1024, 1024, 65, 1024, 1024, 62, 1024, 60, 1024, 1024, 1024, 1024, 55, 54, 53, 1024, 51, 1024, 1024, 1024, 1024, 1024, 45, 1024, 43, 42, 41, 40, 1024, 1024, 37, 1024, 35, 1024, 1024, 32, 31, 30, 1024, 1024, 27, 26, 25, 1024, 1024, 1024, 21, 20, 19, 18, 1024, 16, 1024, 1024, 13, 1024, 1024, 1024, 1024, 8, 1024, 6, 1024, 1024, 3, 2, 1024]
    n = len(v)
    k = sum(v) // n
    b = [0] * n
    ans = [0] * n
    lf = n - k
    for i in range(lf, n):
        b[i] = n - 1
    for i in range(n - 1, -1, -1):
        cur = v[i] - (b[i] - i)
        if cur == i + 1:
            ans[i] = 1
        elif cur == 1:
            ans[i] = 0
            lf -= 1
            b[lf] = i - 1
    print(''.join(map(str, ans)))

solve()