
![all inactive](static/sample.png)

How is it done?
 - all `planets` rotate around a fictional `center of universe (x=0,y=0)`
 - the distance of a planet from the core represents it's solar system position
 - `galaxies` and `solar system` are defined by an angle starting from `x=0` i.g. 12 o'clock
 - `x` and `y` are calculated similar/same as complex numbers
 
```
shift_to_yaxis = pi / 2
galaxy_increment = (2 * pi) / 9 
system_increment = galaxy_increment / 499
minimum_distance = 1
```

the planets start at `x=0`. To match a clock pattern a constant is added to `phi` 
  - `shift_to_yaxis` is set to `pi / 2` (i.e. 90°, here counter clockwise)

```
z = r * e^(i * phi)

phi = f(galaxy, system) = (galaxy - 1) * galaxy_increment + (system - 1) *  system_increment + shift_to_yaxis
x = Re(z)
y = Im(z)
z = x + iy
z = r(cos(phi) + i * sin(phi))

```
usually `r` would be calculated:
```
r = |z| = sqrt(x^2 + y^2)
```

instead we set r to 1 and get our preliminary `x` and `y` values
```
r == 1 
x = cos(phi)
y = sin(phi)
```

adjusting the radius `r` to represent the `slot` in the `solar system`.
`slot = 5` would translates to fifth planet in respective `solar system`

```
r = f(slot) = planet_icrement * slot + minimum_distance
```

final coordinates ready to be plotted

```tex
x = x * r
y = y * r
```

The graph is running counter clockwise which is as expected.
To match it one more step with a clock pattern **the `xaxis` is reversed**.

> Note We never actually touched compley numbers but borrowed the concept!