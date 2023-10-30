import numpy as np


MIN_CALL_GAP = 0

# Selected based on observed trends in human-labeled data
# Few moan have an average slope above fourty. Sixty
# was selected because two components may have a sharper
# drop
# This is a merging criterium
MAX_SLOPE = 60

# When calculating the slope between successive nodes,
# the two nodes sometimes, as in merge, occur at the same
# time. Instead of time being zero, which would result in
# a division by zero, set the time delta to EPSILON.
EPSILON = 0.005



# Constants set in Madhusudhana et al. 2009
U_FREQ_L_BND = 50
L_FREQ_U_BND = 50
MIN_CTR_LEN_T = 0.5
MIN_CTR_LEN_F = 8
MAX_CALL_GAP = 1
SLOPE_L_BND = 10



def processDCalls(contours, merge = True, trim = True, final_rejection = True):
    '''From an array of contours, i.e. a two dimensional array with tuple elements,
    process the D calls similarly to Madhusudhana et al. 2009, removing any contour
    that does not meet the criteria of a D call for a blue whale and trimming excess nodes
    from both ends of each detected tonal.'''

    

    # Remove tonal if max frequency occures after min frequency
    drop = set()
    for i in range(len(contours)):

        contour = np.array(contours[i])

        # Indices of minumum and maximum frequencies
        argmax = contour[:, 1].argmax()
        argmin = contour[:,1].argmin()

        if argmax >= argmin:
            drop.add(i)
        else:
            contours[i] = contours[i][argmax:argmin+1] # Maybe novel, not like Madhusudhana et al. 2009 
    
    contours = [contour.copy() for i, contour in enumerate(contours) if i not in drop]

    # Unlike Madhusudhana et al. 2009, trim before merging contours
    if trim:
        for i in range(len(contours)):
            contours[i] = trimContour(contours[i], SLOPE_L_BND)
    
    
    if merge:
        i = 0
        while i < len(contours) - 1:
            # check for closeness and proper slope
            gap = contours[i+1][0][0]- contours[i][-1][0]
            if (( gap <= MAX_CALL_GAP ) and (gap >= MIN_CALL_GAP)):
                if gap <= 0.0:
                    gap = EPSILON
                slope = (contours[i][-1][1] - contours[i+1][0][1]) / gap
                if ((slope >= 0.9*SLOPE_L_BND) and slope <= MAX_SLOPE):
                    # merge current and next contours
                    contours[i] = contours[i] + contours[i + 1]

                    # remove next contour
                    contours.pop(i+1)
                    # do not increment i since three or more adjacent contours may combine to one
                    continue
            i += 1


    
    # Final rejection criteria
    drop = set()
    rejections = {"kept": 0, "slope": 0, "beginning_freq": 0, "terminating_freq": 0 , "length": 0, "height": 0}
    if final_rejection:
        for i in range(len(contours)):
            contour = contours[i]

            
            # beginning frequency ckeck
            if contour[0][1] < U_FREQ_L_BND:
                drop.add(i)
                rejections["beginning_freq"] += 1

            # terminating frequency check
            if contour[-1][1] > L_FREQ_U_BND:
                drop.add(i)
                rejections["terminating_freq"] += 1
                continue


            # Average slope check
            avg_slope = getAverageSlope(contour)
            if (avg_slope < 0.9 * SLOPE_L_BND):
                drop.add(i)
                rejections["slope"] += 1
                continue

            # long enough in the time dimension
            if contour[-1][0] - contour[0][0] < MIN_CTR_LEN_T:
                drop.add(i)
                rejections["length"] += 1
                continue
            # large enough drop in hz
            if contour[0][1] - contour[-1][1] < MIN_CTR_LEN_F:
                drop.add(i)
                rejections["height"] += 1
                continue
            rejections["kept"] += 1

    # Remove all that were not dropped
    return [contour for i, contour in enumerate(contours) if i not in drop]


def trimContour(contour, SLOPE_L_BND = 10):
    '''Given a contour, which is a list filled with tuples or a 2-D array,
    trims the end points according to the contour trimming algorithm given in
    Madhusudhana et al. 2009. Assumes that the max frequence occures before
    the min frequency in the contour.
    '''

    # Slope is intentionally calculated as its negation
    slope = lambda x1, x2: (contour[x1][1] - contour[x2][1]) / (contour[x2][0] - contour[x1][0])

    low = 0
    high = len(contour) - 1

    change = True
    while change and low < high:
        change = False
        if slope(low, low+1) < 0.9 * SLOPE_L_BND:
            low += 1
            change = True
        if slope(high - 1, high) < 0.9 * SLOPE_L_BND:
            high -= 1
            change = True

    return contour[low:high+1]

def getAverageSlope(contour):
    # Slope is intentionally calculated as its negation
    slope = lambda x1, x2: (contour[x1][1] - contour[x2][1]) / max((contour[x2][0] - contour[x1][0]), EPSILON)
    total = 0
    for i in range(len(contour) - 1):
        total += slope(i, i+1)
    return total / len(contour) - 1

        