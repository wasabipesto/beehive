```js
const thermistors = FileAttachment('thermistors.csv').csv({ typed: true })
```

# Temperature Sensing

There are lots of ways to detect temperature, from old mercury thermometers to bimetallic strips. Most of these rely on some material property that changes as the material heats or cools:

- For mercury thermometers, the mercury expands as the temperature increases, pushing it up along a thin tube for reading.
- For bimetallic strips, two metals that expand at different rates are used to mechanically turn a dial for reading.
- For a thermistor, a resistive element changes resistivity as it heats or cools, allowing rapid electronic measurement.
- For a thermocouple, a pair of conductors produce a measurable voltage when there is a temperature differential between them.
- For a silicon bandgap temperature sensor, the forward voltage of a silicon diode changes with the ambient temperature and can be measured.

## Thermistors

In the HVAC world we need to know the temperature of air and water at dozens of points along its journey into and out of the occupied space in order to control various active devices along the system. The de facto standard for most point air and water sensors is the thermistor due to a number of factors:

its low cost, simple installation, and simple output.

- You can find a thermistor with a standard characteristic resistivity curve in any number of mounting options for $20-50 each. This is less than the labor it costs to install them.
- The accuracy of a thermistor is typically less than one degree Fahrenheit, which is more than sufficient for most applications.
- Each thermistor comes in an assembly for a specific application, such as on the end of an 18" rod for positioning in the center of a duct, inside a shielded enclosure for outdoor air sensing, a metal well with thermally conductive paste for in-pipe sensing, or with a buffer fluid for low-temperature sensing.
- Sensors use one of a few standard "curves" for specific metals and alloys, which most controllers have pre-mapped for automatic conversion.
- Since there are no active powered circuits, there is no power draw and very little that can fail. Sensors can remain in service for over 30 years with little to no degradation.
- Multiple sensors can be averaged together with a simple parallel-series circuit, allowing for arrays of sensors that read as one.

### Thermistor Curves

There are several specific "curves" used by major manufacturers. Some curves are specific to metal alloys, some are calibrated against a specific "reference point" (usually 25°C).

Often you find old sensors in the field connected to old controllers with no documentation or part numbers. If you want to reuse the sensor, you need to figure out what curve it uses and make sure your new controller has the mapping. Below are plots of the most popular curves plotted against each other for easy reference.

<div class="card">

```js
Plot.plot({
  title: 'Resistance vs Temperature',
  width: 830,
  x: { type: 'log' },
  marks: [
    Plot.lineY(thermistors, {
      x: 'ohms',
      y: 'f',
      stroke: 'type',
      tip: true
    })
  ]
})
```

</div>

<div class="card">

```js
Plot.plot({
  title: 'Temperature vs Resistance',
  width: 830,
  y: { type: 'log' },
  marks: [
    Plot.lineY(thermistors, {
      x: 'f',
      y: 'ohms',
      stroke: 'type',
      tip: true
    })
  ]
})
```

</div>

<div class="card">

```js
Plot.plot({
  title: 'Temperature vs Resistance',
  subtitle: 'Zoomed in to typical ambient range',
  width: 830,
  y: { type: 'log' },
  marks: [
    Plot.lineY(
      thermistors.filter((obj) => obj.f >= 55 && obj.f <= 85),
      {
        x: 'f',
        y: 'ohms',
        stroke: 'type',
        tip: true
      }
    )
  ]
})
```

</div>
