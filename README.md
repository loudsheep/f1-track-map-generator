# f1-track-map-generator

Generate SVG track maps of every circuit in a given F1 season

To change season, change this line at the top of `map_generator.py` file
```python
events = fastf1.get_event_schedule(2024, include_testing=False)
```


Generated track map of every circuit will be stored in `tracks/` directory
