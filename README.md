# probably the most unoptimized pixel sorter you will ever see
i only did horizontal sorting because idk

## Needs Fixing
1. make multiprocessing faster
2. fix multiprocessing weirdness
4. better ways to choose bandpass values and not relying on trial and error

## Ideas
1. optional contrast map visualizer (?)
2. GUI (??)
3. different ways of sorting

# requirements
 - numpy
 - tqdm
 - PIL (pillow)

# showcase
works the best with PNG files; lossy compressed image artifacts make it look less appealing 

on the off chance that it actually looks good, this is what it can look like:

### original
![](https://github.com/oaroki-git/worst-pixel-sorter/blob/main/anime_girl_plus_rockets.png)

### sorted
![](https://github.com/oaroki-git/worst-pixel-sorter/blob/main/rockets_sorted.png)

# usage
call the `UIwrapper` function for manual input of parameters, or the `readConfig` function to read a toml file at `~/.config/pixelsort.toml`

# how it works
this pixel sorter follows after [@Acerola_t's pixel sorting video](https://youtu.be/HMmmBDRy-jE?si=xwhLxhm4TeBg9YvG) which uses a contrast map to figure out what to sort.

it's practically a band pass filter where pixels with a grayscale value in the range of (black threshold, white threshold) are candidates to be sorted.

the sorter then sorts each sequence of consecutive sortable pixels in each row horizonally from lowest to highest luminance

# configuration
see [the example toml](https://github.com/oaroki-git/worst-pixel-sorter/blob/main/pixelsort.toml) for a reference
