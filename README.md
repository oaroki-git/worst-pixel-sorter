# probably the most unoptimized pixel sorter you will ever see
i only did horizontal sorting because idk

# requirements
 - numpy
 - tqdm
 - PIL (pillow)

# showcase
works the best with PNG files. 

on the off chance that it actually looks good, this is what it can look like:

### original
![](https://github.com/oaroki-git/worst-pixel-sorter/blob/main/anime_girl_plus_rockets.png)

### sorted
![](https://github.com/oaroki-git/worst-pixel-sorter/blob/main/rockets_sorted.png)

# usage
call the `UIwrapper` function for manual input of parameters, or the `readConfig` function to read a toml file at `~/.config/pixelsort.toml`

# configuration
this pixel sorter follows after [@Acerola_t's pixel sorting video](https://youtu.be/HMmmBDRy-jE?si=xwhLxhm4TeBg9YvG) which uses a contrast map to figure out what to sort.

pixels with a grayscale value in the range (black threshold, white threshold) will be sorted.

see [the example toml](https://github.com/oaroki-git/worst-pixel-sorter/blob/main/pixelsort.toml) for a reference
