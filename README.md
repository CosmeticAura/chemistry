# studynow

The kit behind my class study sites, like [chemistry](https://cosmeticaura.github.io/chemistry/).

Each class gets a home page, one study loop page per unit (read, break, flashcards, break, brain dump, mark) and a review page once there are two or more units.

- `unit.html` is the study loop page
- `home.html` is the home page shell
- `build.py` turns a `course.py` into the whole site

```
python3 build.py course.py site
```
