### Why do we use suffixes like `_model`, `_repo`, `_service`, and `_route` in file names?

Here’s a side-by-side comparison of what your file structure would look like **with** and **without** suffixes for the `user` module:

### With suffixes (what you're using)

```
backend/app/
├── api/
│   └── route/
│       └── user_route.py
├── service/
│   └── user_service.py
├── model/
│   └── user_model.py
├── data/
│   └── repo/
│       └── user_repo.py
```

---

### Without suffixes

```
backend/app/
├── api/
│   └── route/
│       └── user.py
├── service/
│   └── user.py
├── model/
│   └── user.py
├── data/
│   └── repo/
│       └── user.py
```

### Why suffixes win

In small projects, the shorter names are fine. But once your project grows and you open multiple `user.py` files in your IDE, it becomes harder to know which is which. The suffix-based naming makes each file’s purpose instantly clear and avoids confusion. It significantly improves navigation and search. 


### Why are repositories registered as providers.Factory instead of Singleton?
Why do you use `providers.Factory` for repositories and `services`? Wouldn’t Singleton be more efficient?

- when statelss we use singleton. If not we use factory.


### Why do we raise custom exceptions from both services and routes?