# ProShop — Django + React E-Commerce (Udemy Course Notes)

> **Course:** [Django with React | An Ecommerce Website](https://www.udemy.com/course/django-with-react-an-ecommerce-website/)
> **Stack:** Django REST Framework (backend) + React SPA (frontend)
> **Purpose:** Personal learning log — concepts, decisions, and code structure explained section by section.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Section 1 — Project Setup & Frontend Scaffold](#section-1--project-setup--frontend-scaffold)
- [Section 2 — Starting the Front End](#section-2--starting-the-front-end)

---

## Project Overview

A full-stack e-commerce web app called **ProShop** built with:

| Layer | Technology |
|---|---|
| Backend | Django + Django REST Framework |
| Frontend | React (Create React App) |
| Styling | React Bootstrap + Font Awesome |
| Communication | Axios (React → Django REST API) |
| State Management | Redux (to be added) |

### How the two sides connect
- Django serves a REST API (JSON responses)
- React is a SPA (Single Page Application) — one HTML file, JS handles all navigation
- React fetches data from Django via HTTP requests (axios)
- They run as two separate servers in development

---

## Section 1 — Project Setup & Frontend Scaffold

### What was built

The foundational layout shell of the React frontend.

**Files created:**
- `frontend/src/App.js` — root component, layout shell
- `frontend/src/components/Header.jsx` — top navigation bar
- `frontend/src/components/Footer.jsx` — copyright footer

---

### App.js — The Layout Shell

```jsx
import { Container } from 'react-bootstrap'
import Header from "./ components/Header";
import Footer from "./ components/Footer";

function App() {
  return (
    <div>
      <Header />
      <main className='py-3'>
        <Container>
          <h1>Welcome</h1>
        </Container>
      </main>
      <Footer />
    </div>
  );
}
```

**What it does:**
- Acts as the permanent wrapper for the entire app
- `Header` and `Footer` are always visible regardless of what page you're on
- The `<main>` block in the middle is where page content will load (React Router will plug routes in here later)
- `Container` from React Bootstrap keeps content centered with a max-width

---

### Header.jsx — Navigation Bar

```jsx
<Navbar bg="dark" variant="dark" expand="lg" collapseOnSelect>
  <Container>
    <Navbar.Brand href="/">ProShop</Navbar.Brand>
    <Navbar.Toggle aria-controls="basic-navbar-nav" />
    <Navbar.Collapse id="basic-navbar-nav">
      <Nav className="mr-auto">
        <Nav.Link href="/cart"><i className="fas fa-shopping-cart"></i>Cart</Nav.Link>
        <Nav.Link href="/login"><i className="fas fa-user"></i>Login</Nav.Link>
      </Nav>
    </Navbar.Collapse>
  </Container>
</Navbar>
```

**What it does:**
- Dark themed navbar using React Bootstrap's `Navbar` component
- `Navbar.Toggle` is the hamburger button — appears on mobile, collapses/expands nav links
- `collapseOnSelect` closes the mobile menu when a link is clicked
- Cart and Login links use Font Awesome icons (`fas fa-*`)
- Links currently use plain `href` — will be replaced with React Router's `<Link>` later

---

### Footer.jsx — Copyright Bar

```jsx
<footer>
  <Container>
    <Row>
      <Col className="text-center py-3">Copyright &copy; ProShop</Col>
    </Row>
  </Container>
</footer>
```

**What it does:**
- Simple centered copyright line
- Uses Bootstrap grid (`Container > Row > Col`) for layout
- `py-3` adds vertical padding

---

### Key Concepts from this Section

**React Components**
- Everything in React is a component — a JS function that returns JSX (HTML-like syntax)
- Components are reusable and composable (you put them inside each other)
- `App.js` is the root component; `Header` and `Footer` are child components

**SPA Architecture**
- React loads one `index.html` file in the browser — ever
- Navigation swaps components in/out without reloading the page
- React Router (added later) handles URL → component mapping

**React Bootstrap**
- Pre-built components (`Navbar`, `Container`, `Row`, `Col`) that output responsive Bootstrap HTML
- Saves writing raw HTML + Bootstrap classes manually

**`.js` vs `.jsx`**
- No functional difference in Create React App projects
- Both can contain JSX syntax — it's purely a naming convention

---

---

## Section 2 — Starting the Front End

### What was built

The full frontend — product grid, product detail page, routing, and reusable components.

**Files created:**
- `frontend/src/products.js` — hardcoded product data (temporary, replaced by Django API later)
- `frontend/src/pages/HomeScreen.jsx` — homepage, renders the product grid
- `frontend/src/pages/ProductScreen.jsx` — product detail page
- `frontend/src/components/Product.jsx` — single product card component
- `frontend/src/components/Rating.jsx` — reusable star rating display component

**Files updated:**
- `frontend/src/App.js` — added React Router (Router, Routes, Route) and all page routes

---

### products.js — Temporary Data

```js
const products = [
  {
    '_id': '1',
    'name': 'Airpods Wireless Bluetooth Headphones',
    'image': '/images/airpods.jpg',
    'price': 89.99,
    'rating': 4.5,
    'numReviews': 12,
    // ...more fields
  },
  // ...more products
]
export default products
```

**What it does:**
- A plain JS array of product objects exported as a default export
- Acts as a stand-in for the Django REST API — same data shape will come from the backend later
- Each product has: `_id`, `name`, `image`, `description`, `brand`, `category`, `price`, `countInStock`, `rating`, `numReviews`
- Using `_id` (MongoDB-style) rather than `id` to match what Django will return

---

### HomeScreen.jsx — Product Grid Page

```jsx
export default function HomeScreen() {
  return (
    <div>
      <h1>Latest Product</h1>
      <Row>
        {products.map((p) => (
          <Col sm={12} md={6} lg={4} xl={3} key={p._id}>
            <Product product={p} />
          </Col>
        ))}
      </Row>
    </div>
  );
}
```

**What it does:**
- Loops over the `products` array using `.map()` and renders a `<Product>` card for each one
- Uses Bootstrap's responsive grid — `Col` breakpoints control how many cards appear per row:
  - Mobile (`sm`): 1 card per row (full width)
  - Tablet (`md`): 2 cards per row
  - Desktop (`lg`): 3 cards per row
  - Wide (`xl`): 4 cards per row
- `key={p._id}` is required by React when rendering lists — it helps React track which item is which when the list updates

---

### Product.jsx — Product Card

```jsx
export default function Product({ product }) {
  return (
    <Card className="my-3 p-3 rounded border border-secondary">
      <a href={`/product/${product._id}`}>
        <Card.Img src={product.image} />
      </a>
      <Card.Body>
        <a href={`/product/${product._id}`}>
          <Card.Title as="div">
            <strong>{product.name}</strong>
          </Card.Title>
        </a>
        <Card.Text as="div">
          <div className="my-3">
            <Rating value={product.rating} text={`${product.numReviews} reviews`} color={"#f8e825"} />
          </div>
        </Card.Text>
        <Card.Text>
          <h3>${product.price}</h3>
        </Card.Text>
      </Card.Body>
    </Card>
  );
}
```

**What it does:**
- Receives a single `product` object as a **prop** (data passed in from the parent `HomeScreen`)
- Renders a Bootstrap `Card` with: product image, name, star rating, and price
- Both the image and name are wrapped in `<a>` tags linking to `/product/:id` — the product detail page (built later)
- `Card.Title as="div"` renders the title as a `<div>` instead of the default `<h5>` — avoids invalid HTML nesting
- `Rating` is passed `value`, `text`, and `color` as props

**Props concept:**
Props are how a parent component passes data down to a child. `HomeScreen` passes each product object into `Product` — `Product` receives it and displays it. Data always flows **down** (parent → child), never up.

---

### Rating.jsx — Star Rating Display

```jsx
export default function Rating({ value, text, color }) {
  return (
    <div className="rating">
      <span>
        <i style={{ color }} className={
          value >= 1 ? "fas fa-star" : value >= 0.5 ? "fas fa-star-half-alt" : "far fa-star"
        }></i>
      </span>
      {/* repeated for stars 2–5, thresholds increase by 1 each time */}
      <span>{text && text}</span>
    </div>
  );
}
```

**What it does:**
- Renders 5 stars using Font Awesome icons, each conditionally styled based on `value`
- Three possible states per star:
  - `fas fa-star` → full star (solid)
  - `fas fa-star-half-alt` → half star
  - `far fa-star` → empty star (outline)
- `style={{ color }}` applies the passed-in color (e.g. `#f8e825` yellow) inline
- `{text && text}` — only renders the review count text if `text` was passed in (short-circuit evaluation)

**The star logic per position:**
| Star | Full if | Half if |
|---|---|---|
| 1 | value >= 1 | value >= 0.5 |
| 2 | value >= 2 | value >= 1.5 |
| 3 | value >= 3 | value >= 2.5 |
| 4 | value >= 4 | value >= 3.5 |
| 5 | value >= 5 | value >= 4.5 |

**Important bug to watch:** The empty star class must be `far fa-star` (Font Awesome Regular), NOT `fas fa-star` (Font Awesome Solid). Using `fas` for empty stars renders a full star — always double-check the prefix.

---

### Key Concepts from this Section

**Props**
- Short for "properties" — the way a parent passes data into a child component
- Read-only inside the child (you never modify props directly)
- Any JS value can be a prop: strings, numbers, objects, arrays, functions

**`.map()` for rendering lists**
- The standard React pattern for rendering a list of components from an array
- Always needs a unique `key` prop on the outermost element — React uses it internally for efficient re-rendering

**Conditional rendering with ternary**
- `condition ? valueIfTrue : valueIfFalse` is used heavily in JSX since you can't use `if/else` directly inside JSX
- Can be chained: `a ? x : b ? y : z`

**Short-circuit evaluation**
- `{text && text}` means: if `text` is truthy, render it — otherwise render nothing
- Common React pattern for optionally rendering parts of the UI

**Responsive Bootstrap grid**
- `Col` accepts breakpoint props (`sm`, `md`, `lg`, `xl`) that define column width at each screen size
- Bootstrap uses a 12-column grid — `xl={3}` means "take up 3 of 12 columns" = 4 cards per row

**Component tree so far:**
```
App
├── Header
├── main
│   └── HomeScreen
│       └── Product (×6)
│           └── Rating
└── Footer
```

---

---

### App.js — Routing Setup

```jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <Router>
      <Header />
      <main className='py-3'>
        <Container>
          <Routes>
            <Route path='/' element={<HomeScreen />} />
            <Route path='/product/:id' element={<ProductScreen />} />
          </Routes>
        </Container>
      </main>
      <Footer />
    </Router>
  );
}
```

**What it does:**
- `<Router>` wraps the entire app — required so that `<Link>` components anywhere in the tree (including `Header`) have access to routing context
- `<Routes>` wraps only the swappable content area — `Header` and `Footer` sit outside it so they stay permanently visible
- Two routes defined:
  - `/` → renders `HomeScreen`
  - `/product/:id` → renders `ProductScreen`, where `:id` is a dynamic URL parameter

**Why `Router` wraps everything and not just `Routes`:**
`Header` contains `<Link>` components which need the Router context. If `Router` only wrapped `Routes`, the Header links would break.

---

### Route vs Link

| | `<Route>` | `<Link>` |
|---|---|---|
| Lives in | `App.js` | Any component |
| Purpose | Defines what renders at a URL | Changes the URL when clicked |
| Visible to user | No — purely logical | Yes — renders as `<a>` tag |
| Triggers navigation | No | Yes |

**The chain:**
```
User clicks <Link to="/product/3">
        ↓
URL changes to /product/3 (no page reload)
        ↓
<Route path='/product/:id'> matches
        ↓
<ProductScreen /> renders
```

---

### Dynamic URL params — `:id`

The `:` in `/product/:id` tells React Router this segment is a **variable**, not a literal string.

- `/product/1` → matches, captures `id = "1"`
- `/product/42` → matches, captures `id = "42"`
- `/product` → does NOT match (missing the id segment)

Without `:id` the route would only match `/product` exactly — useless since you need to know which product to show.

**Reading the param inside the component:**

```jsx
// v5 (old course syntax — does NOT work in v6/v7)
export default function ProductScreen({ match }) {
  const product = products.find((p) => p._id == match.params.id)
}

// v6/v7 (correct)
import { useParams } from 'react-router-dom'

export default function ProductScreen() {
  const { id } = useParams()
  const product = products.find((p) => p._id === id)
}
```

`useParams()` is a **hook** — a React function that reads data from the current context. In v6+ all route data is accessed via hooks, not props.

---

### ProductScreen.jsx — Product Detail Page

```jsx
export default function ProductScreen() {
  const { id } = useParams()
  const product = products.find((p) => p._id === id)

  return (
    <div>
      <Link to="/" className="btn btn-light my-3">Go Back</Link>
      <Row>
        <Col md={6}>
          <Image src={product.image} alt={product.name} fluid />
        </Col>
        <Col md={3}>
          <ListGroup variant="flush">
            <ListGroup.Item><h3>{product.name}</h3></ListGroup.Item>
            <ListGroup.Item>
              <Rating value={product.rating} text={`${product.numReviews} reviews`} color="#f8e825" />
            </ListGroup.Item>
            <ListGroup.Item>Price: ${product.price}</ListGroup.Item>
            <ListGroup.Item>Description: {product.description}</ListGroup.Item>
          </ListGroup>
        </Col>
        <Col md={3}>
          <Card>
            <ListGroup variant="flush">
              <ListGroup.Item>
                <Row>
                  <Col>Price:</Col>
                  <Col><strong>${product.price}</strong></Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <Row>
                  <Col>Stock:</Col>
                  <Col>{product.countInStock > 0 ? 'In Stock' : 'Out of Stock'}</Col>
                </Row>
              </ListGroup.Item>
              <ListGroup.Item>
                <Button className="w-100" type="button" disabled={product.countInStock === 0}>
                  Add to cart
                </Button>
              </ListGroup.Item>
            </ListGroup>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
```

**Layout — 3 column structure:**
```
| Col md=6        | Col md=3         | Col md=3        |
| Product image   | Details list     | Purchase card   |
|                 | - Name           | - Price         |
|                 | - Rating         | - Stock status  |
|                 | - Price          | - Add to cart   |
|                 | - Description    |                 |
```

**Key parts:**
- `<Image fluid />` — Bootstrap responsive image, scales to fit its container
- `<ListGroup variant="flush">` — removes outer borders so the list sits cleanly inside a `Card`
- Stock status uses ternary: `countInStock > 0 ? 'In Stock' : 'Out of Stock'`
- `disabled={product.countInStock === 0}` — disables the button when out of stock, Bootstrap greys it out automatically
- `<Link to="/">` styled as a button via Bootstrap classes (`btn btn-light`) — it's still a link, just looks like a button

---

### Bootstrap Version Gotchas (v4 → v5)

This course was recorded with Bootstrap 4. You're running Bootstrap 5 (via Bootswatch Lux theme). Two differences already encountered:

| Bootstrap 4 | Bootstrap 5 equivalent |
|---|---|
| `className="btn-block"` | `className="w-100"` or wrap in `<div className="d-grid">` |
| `btn-block` makes full width | `w-100` sets `width: 100%` |

Watch for similar small class name changes as the course progresses.

---

### Key Concepts from this Section

**React Router v6/v7 vs v5**
- v5 injected `match`, `history`, `location` as props — no longer works
- v6/v7 uses hooks: `useParams()`, `useNavigate()`, `useLocation()`
- Always use `element={<Component />}` not `component={Component}`

**`useParams()` hook**
- Reads dynamic URL segments defined with `:` in the route path
- Returns an object — destructure the param name you defined: `const { id } = useParams()`
- The name must match exactly: route says `:id` → `useParams()` returns `{ id }`

**`<Image fluid />`**
- React Bootstrap's responsive image component
- `fluid` prop adds `max-width: 100%` so image never overflows its container

**`<ListGroup variant="flush">`**
- Removes the outer border and rounded corners from the list group
- Used when the list sits inside a `Card` so it blends in cleanly

**Updated component tree:**
```
App (Router)
├── Header
├── main
│   └── Routes
│       ├── / → HomeScreen
│       │       └── Product (×6)
│       │               └── Rating
│       └── /product/:id → ProductScreen
│                               └── Rating
└── Footer
```

---

---

## Section 3 — Django Backend & Connecting React to the API

### What was built

The Django REST Framework backend with three API endpoints, and the React frontend updated to fetch real data from those endpoints instead of the hardcoded `products.js` file.

**Files created:**
- `backend/` — new Django project folder (created with `django-admin startproject backend`)
- `backend/api/` — Django app (created with `python manage.py startapp api`)
- `backend/api/products.py` — temporary hardcoded product data (mirrors the old `frontend/src/products.js`)
- `backend/api/views.py` — three Class Based Views (APIView)
- `backend/api/urls.py` — URL patterns for the `api` app

**Files updated:**
- `backend/backend/settings.py` — registered `rest_framework`, `corsheaders`, and `api` app; added CORS config
- `backend/backend/urls.py` — wired `api/` prefix to `api.urls`
- `frontend/src/pages/HomeScreen.jsx` — replaced static import with `useState` + `useEffect` + axios
- `frontend/src/pages/ProductScreen.jsx` — same pattern, fetches single product by id

---

### settings.py — Registering apps and CORS

```python
INSTALLED_APPS = [
    # Django built-ins ...
    'api.apps.ApiConfig',   # our app
    'rest_framework',       # DRF
    'corsheaders'           # CORS headers
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",   # must be near the top
    "django.middleware.common.CommonMiddleware",
    # ... rest of middleware
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

**What CORS is and why it's needed:**

By default browsers block JavaScript on one origin (e.g. `localhost:3000`) from reading responses from a different origin (`localhost:8000`). This is the browser's Same-Origin Policy — a security feature.

`django-cors-headers` adds the right HTTP headers to Django's responses to tell the browser "this origin is allowed to read my responses".

```
React (port 3000)  ──GET /api/products/──►  Django (port 8000)
                   ◄──Access-Control-Allow-Origin: localhost:3000──
                                 ↑
                   corsheaders adds this header
```

Without it, axios gets the data but the browser refuses to hand it to your JS code.

**Why `CorsMiddleware` must be near the top:**
Django runs middleware top-to-bottom on every request. CORS headers need to be added before any other middleware might short-circuit the response (e.g. returning a 403). Placing it second (after `SecurityMiddleware`) guarantees it always runs.

---

### URL routing — two-level system

Django URL routing is split across two files:

```
backend/backend/urls.py          backend/api/urls.py
───────────────────────          ────────────────────────────────────
admin/  → admin site             ''           → GetRoutes
api/    ──include()──────────►   products/    → GetProducts
                                 products/<str:pk> → GetProduct
```

**backend/backend/urls.py** (the project-level router):
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # hands off anything starting with api/ to api/urls.py
]
```

**backend/api/urls.py** (the app-level router):
```python
urlpatterns = [
    path('', views.GetRoutes.as_view(), name='get_routes'),
    path('products/', views.GetProducts.as_view(), name='get_products'),
    path('products/<str:pk>', views.GetProduct.as_view(), name='get_product'),
]
```

The `<str:pk>` in the last path is a **URL parameter** — same idea as React Router's `:id`. Django captures whatever string is in that position and passes it to the view as `pk`.

**The `.as_view()` call:**
FBVs are just functions — you reference them directly. CBVs are classes — `.as_view()` converts the class into a callable function that Django's URL system can use. Without it you'd get an error.

| FBV url wiring | CBV url wiring |
|---|---|
| `path('', views.get_products)` | `path('', views.GetProducts.as_view())` |

---

### views.py — Class Based Views (APIView)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .products import products


class GetRoutes(APIView):
    def get(self, request):
        routes = [
            'GET /api/products',
            'GET /api/products/<id>',
        ]
        return Response(routes)


class GetProducts(APIView):
    def get(self, request):
        return Response(products)


class GetProduct(APIView):
    def get(self, request, pk):
        try:
            product = [p for p in products if p['_id'] == pk][0]
        except IndexError:
            product = None
        return Response(product)
```

**Why `class` not `def`:**
In the tutorial the instructor writes `@api_view(['GET']) def getProducts(request)`. Here you're using CBVs instead. The HTTP method (`GET`) becomes a method named `get` on the class. Django calls the right method automatically based on the incoming request type.

**`APIView` vs plain Django `View`:**
`APIView` comes from Django REST Framework and adds:
- Automatic JSON parsing of incoming request bodies
- `Response()` — a DRF response that handles content negotiation (returns JSON by default)
- The browsable API UI (visit `localhost:8000/api/products/` in the browser to see it)

**`GetProduct` — finding by pk:**
```python
product = [p for p in products if p['_id'] == pk][0]
```
This is a **list comprehension** — it loops over `products`, keeps only the ones where `_id` matches `pk`, then takes the first result (`[0]`). If nothing matches, `[0]` raises an `IndexError`, which is caught and returns `None`.

---

### Frontend — useState + useEffect + axios pattern

Both `HomeScreen` and `ProductScreen` now follow the same pattern for fetching data from the API:

```jsx
// HomeScreen.jsx
const [products, setProducts] = useState([]);  // [] = empty array while loading

useEffect(() => {
  async function fetchProducts() {
    const { data } = await axios.get('/api/products/');
    setProducts(data);
  }
  fetchProducts();
}, []);  // [] = only run once, when the component first mounts
```

```jsx
// ProductScreen.jsx
const { id } = useParams();
const [product, setProduct] = useState('');  // empty while loading

useEffect(() => {
  async function getProduct(id) {
    const { data } = await axios.get(`/api/products/${id}`);
    setProduct(data);
  }
  getProduct(id);
}, [id]);  // re-run if id changes (user navigates to a different product)
```

**The render cycle with async data:**
```
1. Component renders → products = [] (empty, nothing displayed yet)
2. useEffect runs after render → axios fetches from Django
3. Django responds with JSON → setProducts(data) called
4. React re-renders → products = [...] → cards appear on screen
```

This is why `useState([])` matters — on step 1, React tries to call `.map()` on whatever the initial state is. If it's `undefined` (no default), `.map()` crashes. An empty array `[]` is safe to `.map()` over — it just renders nothing until data arrives.

**The dependency array `[]`:**

| `useEffect(() => {...})` | No array — runs after every render (infinite loop risk) |
|---|---|
| `useEffect(() => {...}, [])` | Empty array — runs once on mount only |
| `useEffect(() => {...}, [id])` | Runs when `id` changes |

`ProductScreen` uses `[id]` so if the user navigates directly from one product page to another, the fetch re-runs for the new id.

**Proxy vs CORS:**
The `"proxy": "http://127.0.0.1:8000"` in `frontend/package.json` forwards API requests in development so axios can call `/api/products/` (relative URL) instead of `http://127.0.0.1:8000/api/products/` (absolute). The CORS setup in Django is still needed for when you eventually build and deploy, or if the proxy doesn't forward correctly.

---

### Bugs caught and fixed in this section

| Bug | Cause | Fix |
|---|---|---|
| `urlpattern` not found | Typo — missing `s` | `urlpatterns` |
| `path('', include('api.urls'))` → 404 on `/api/` | api app mounted at root, not at `api/` | `path('api/', include('api.urls'))` |
| `def getRoutes(APIView)` | Wrote a function with a parameter, not a class | `class GetRoutes(APIView):` |
| `products.map is not a function` | `useState()` starts as `undefined` | `useState([])` |
| `useEffect` runs infinitely | Missing dependency array | Add `[]` as second argument |
| `getProduct()` called without argument | Function defined with `id` param but called with nothing | `getProduct(id)` |

---

### Key Concepts from this Section

**Django REST Framework (DRF)**
- A library built on top of Django that makes building JSON APIs much easier
- Provides `APIView`, `Response`, serializers, and the browsable API UI
- Install: `pip install djangorestframework`

**Class Based Views (CBV) vs Function Based Views (FBV)**
- FBV: one function per endpoint, decorated with `@api_view`
- CBV: one class per endpoint, HTTP methods become class methods (`get`, `post`, `put`, `delete`)
- CBVs are more structured and easier to extend, but slightly more verbose for simple cases
- URL wiring difference: CBVs require `.as_view()`, FBVs do not

**`useEffect` hook**
- Runs side effects (fetching data, subscriptions, timers) after the component renders
- The dependency array controls when it re-runs
- Never put `async` directly on the `useEffect` callback — define an inner async function and call it

**`useState` initial value matters**
- The initial value is what React renders with on the very first render, before any data arrives
- Arrays of things → `[]`, single objects → `{}` or `null`, strings → `''`
- Using no default (`useState()`) gives `undefined`, which crashes any `.map()` or property access

---

### Sections 14–17 — Database Setup, Models, Image Field & Static Files

**Files created/updated:**
- `backend/api/models.py` — five Django models (Product, Review, Order, OrderItem, ShippingAddress)
- `backend/api/admin.py` — registered all models with the admin panel
- `backend/api/migrations/` — auto-generated migration files (one per change)
- `backend/backend/settings.py` — added `MEDIA_URL`, `MEDIA_ROOT`, `STATIC_FILES_DIRS`

---

### The Django database workflow

Every time you change `models.py`, you follow the same two-step command sequence:

```
1. python manage.py makemigrations
   → Django reads models.py and writes a migration file (a Python script describing the change)

2. python manage.py migrate
   → Django runs those migration files against the database (SQLite by default)
```

Think of migrations as a version history for your database schema — each file records one set of changes so the database can be updated incrementally without losing data.

```
models.py  ──makemigrations──►  migrations/0001_initial.py
                                migrations/0002_alter_product_rating.py
                                migrations/0003_order_orderitem_review_...py
                                migrations/0004_product_image.py
                                        │
                                  migrate▼
                                    db.sqlite3  (actual database)
```

---

### The Admin Panel

Django ships with a built-in admin UI at `/admin/`. To use it:

```bash
python manage.py createsuperuser   # creates a login account
```

To make your models appear in the admin:

```python
# admin.py
from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
```

`from .models import *` imports all models at once. Each `register()` call tells Django's admin to expose that model — you can then create, read, update, and delete records through the browser UI without writing any views.

`__str__` on each model controls how a record displays in the admin list:
```python
def __str__(self):
    return self.name   # Product shows its name in the list
```

---

### models.py — Field types explained (once each)

```python
class Product(models.Model):
    user        = models.ForeignKey(...)
    name        = models.CharField(max_length=200, null=True, blank=True)
    image       = models.ImageField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating      = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews  = models.IntegerField(null=True, blank=True, default=0)
    isPaid      = models.BooleanField(default=False)
    createdAt   = models.DateTimeField(auto_now_add=True)
    _id         = models.AutoField(primary_key=True, editable=False)
```

| Field type | Used for | Key options |
|---|---|---|
| `CharField` | Short text (names, titles) | `max_length` required |
| `TextField` | Long text (descriptions, comments) | No max length |
| `IntegerField` | Whole numbers | `default=0` common |
| `DecimalField` | Precise numbers (money) | `max_digits`, `decimal_places` both required |
| `BooleanField` | True/False | `default=False` common |
| `DateTimeField` | Date + time | `auto_now_add=True` = set once on create |
| `ImageField` | Image file upload | Stores the file path, not the file itself |
| `AutoField` | Auto-incrementing integer | Used here as custom primary key `_id` |

**`null=True` vs `blank=True` — they do different things:**

| Option | Controls | Where |
|---|---|---|
| `null=True` | Database level — the column can store NULL | SQLite/Postgres |
| `blank=True` | Validation level — the field can be left empty in forms/admin | Django forms |

You almost always use both together. Using only `null=True` means the DB accepts NULL but Django's form validation still rejects empty submissions.

**`auto_now_add=True`** — sets the timestamp automatically the moment a record is created. You cannot edit it afterwards (that's what `auto_now_add=False, blank=True, null=True` is for — a nullable datetime you control manually, like `paidAt`).

**`_id = models.AutoField(primary_key=True, editable=False)`** — Django normally creates an `id` field automatically. Here it's overridden with `_id` to match the MongoDB-style naming used in the frontend from earlier. `editable=False` hides it from forms and admin.

---

### Relationships between models

The data model has three types of relationships:

**ForeignKey — many-to-one**
```python
# Review → Product (many reviews can belong to one product)
product = models.ForeignKey(to=Product, on_delete=models.SET_NULL, null=True)
```
Many reviews can point to one product, but each review only points to one product.

`on_delete=models.SET_NULL` — if the referenced product is deleted, set this field to NULL instead of deleting the review too. Requires `null=True`.

Other `on_delete` options:
| Option | Effect when parent is deleted |
|---|---|
| `CASCADE` | Delete this record too |
| `SET_NULL` | Set field to NULL (requires `null=True`) |
| `PROTECT` | Block deletion of parent if children exist |

**OneToOneField — one-to-one**
```python
# ShippingAddress → Order (each order has exactly one shipping address)
order = models.OneToOneField(to=Order, on_delete=models.CASCADE, null=True, blank=True)
```
Like ForeignKey but enforces uniqueness — you can't attach two shipping addresses to the same order.

`CASCADE` here means: if the order is deleted, delete its shipping address too. Makes sense since an address without an order is meaningless.

**Built-in `User` model**
```python
from django.contrib.auth.models import User

user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
```
Django ships with a `User` model (with username, password, email etc.) already built. You don't rewrite it — you just import and reference it. Products, Reviews, and Orders all link to `User` this way.

**Full relationship map:**
```
User ──────────────────────────────────┐
 │                                     │
 ├──(FK)──► Product ◄──(FK)── Review   │
 │               ▲                     │
 │               │                     │
 └──(FK)──► Order ──(1:1)──► ShippingAddress
                 │
                 └──(FK)── OrderItem ──(FK)──► Product
```

---

### ImageField & Static Files (sections 16–17)

**Why ImageField needs an extra package:**
Django's `ImageField` validates that the uploaded file is actually an image. This requires `Pillow`:
```bash
pip install Pillow
```
Without Pillow, `makemigrations` will error when it sees `ImageField`.

**settings.py additions:**
```python
MEDIA_URL = '/images/'         # URL prefix for serving uploaded files
MEDIA_ROOT = 'static/images'   # where files are actually saved on disk

STATIC_FILES_DIRS = [
    BASE_DIR / 'static'        # where Django looks for static assets (CSS, JS, images)
]
```

```
Browser requests /images/airpods.jpg
        ↓
Django maps MEDIA_URL → MEDIA_ROOT
        ↓
Reads from: backend/static/images/airpods.jpg
```

**Static vs Media files:**

| | Static files | Media files |
|---|---|---|
| What | CSS, JS, hardcoded images | User-uploaded files |
| Setting | `STATIC_URL`, `STATICFILES_DIRS` | `MEDIA_URL`, `MEDIA_ROOT` |
| Changes | Only when you redeploy | Any time a user uploads |

---

### Serializers — connecting the database to JSON

**Files created/updated:**
- `backend/api/serializers.py` — `ProductSerializer` using `ModelSerializer`
- `backend/api/views.py` — updated `GetProducts` and `GetProduct` to serialize QuerySet data before returning it

**Why serializers are needed:**

When Django queries the database it returns **Python objects** (QuerySet instances), not JSON. `Response()` can't send Python objects over HTTP — it needs plain data (dicts, lists, strings).

A serializer converts in both directions:

```
Database QuerySet ──serialize──► Python dict ──► JSON   (reading)
JSON              ──deserialize──► Python dict ──► save()  (writing)
```

Without a serializer you'd get an error like:
```
Object of type Product is not JSON serializable
```

**serializers.py:**

```python
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
```

`ModelSerializer` reads your model definition and auto-generates all the fields for you — you don't list them manually.

`class Meta` is an inner class that configures the serializer:

| Meta option | What it does |
|---|---|
| `model = Product` | Which model to base the serializer on |
| `fields = '__all__'` | Include every field from the model |
| `fields = ['name', 'price']` | Alternative — include only listed fields |
| `exclude = ['_id']` | Alternative — include everything except listed fields |

**views.py — before and after:**

```python
# Before — returning a raw QuerySet (broken)
def get(self, request):
    products = Product.objects.all()
    return Response(products)   # ✗ can't serialize QuerySet objects

# After — passing through the serializer first
def get(self, request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)   # ✓ serializer.data is a plain dict/list
```

**The `many` argument:**

| Situation | Argument |
|---|---|
| Serializing a list / QuerySet | `many=True` |
| Serializing a single object | `many=False` (default, can be omitted) |

**`serializer.data`** is the final converted output — a Python dict (or list of dicts) that `Response()` turns into JSON and sends to the browser.

**Full data flow with serializer:**

```
Browser GET /api/products/
        ↓
GetProducts.get()
        ↓
Product.objects.all()  →  QuerySet [<Product>, <Product>, ...]
        ↓
ProductSerializer(queryset, many=True)
        ↓
serializer.data  →  [{'_id': 1, 'name': 'Airpods', ...}, {...}]
        ↓
Response(serializer.data)  →  JSON sent to browser
        ↓
React axios receives data → setProducts(data) → renders cards
```

---

## Section 4 — Implementing Redux for State Management

### What was built

A Redux store wired into the React app, with the first action/reducer pair for fetching the product list from Django.

**Files created:**
- `frontend/src/Store.jsx` — creates and exports the Redux store
- `frontend/src/constants/productConstants.js` — shared string constants for action types
- `frontend/src/reducers/productReducers.js` — reducer for the product list slice of state
- `frontend/src/actions/productActions.js` — async action creator that fetches from Django

**Files updated:**
- `frontend/src/index.js` — wrapped `<App>` in `<Provider store={store}>`

---

### Why Redux — the problem it solves

Before Redux, each component managed its own local state and fetched its own data:

```js
// HomeScreen — had to fetch for itself
const [products, setProducts] = useState([])
useEffect(() => { axios.get('/api/products/').then(...) }, [])
```

This works for one screen. But in a full app:
- The cart count needs to show in `<Header>` AND on the cart page
- User login state is needed in `<Header>`, checkout, and profile
- You'd have to lift state up to `<App>` and prop-drill it down everywhere

Redux fixes this with a **single store** that any component can read from directly:

```
Before Redux                     After Redux
────────────────────             ──────────────────────────
App (holds all state)            Redux Store (holds all state)
 ├─ Header (gets user            ├─ Header ──useSelector──► store.userLogin
 │   via props ↑↑↑)             ├─ HomeScreen ──useSelector──► store.productList
 ├─ HomeScreen (gets             └─ CartScreen ──useSelector──► store.cart
 │   products via props ↑)
 └─ CartScreen (gets
     cart via props ↑↑)
```

---

### The four files and what each one does

#### 1. `productConstants.js` — shared labels

```js
export const PRODUCT_LIST_REQUEST = 'PRODUCT_LIST_REQUEST'
export const PRODUCT_LIST_SUCCESS = 'PRODUCT_LIST_SUCCESS'
export const PRODUCT_LIST_FAIL    = 'PRODUCT_LIST_FAIL'
```

Just strings. Imported by both the action and the reducer so they always use the exact same value. If you typed the string manually in both files and made a typo in one, the action and reducer would never match — a silent bug. A shared constant turns that into an import error instead.

#### 2. `productReducers.js` — how state changes

```js
export const productListReducers = (state = { products: [] }, action) => {
    switch (action.type) {
        case PRODUCT_LIST_REQUEST:
            return { loading: true, products: [] }
        case PRODUCT_LIST_SUCCESS:
            return { loading: false, products: action.payload }
        case PRODUCT_LIST_FAIL:
            return { loading: false, error: action.payload }
        default:
            return state
    }
}
```

The reducer is a **pure function** — no API calls, no side effects. It just receives the current state and an action, and returns a new state object. Redux calls it automatically every time an action is dispatched.

`state = { products: [] }` — the default parameter sets the initial state for this slice. On first load, before any action is dispatched, the store starts with `{ products: [] }`.

The `switch` compares `action.type` (a string) against the constants. When one matches it returns a new object — it never mutates the existing state.

#### 3. `productActions.js` — the async work

```js
export const listProducts = () => async (dispatch) => {
    try {
        dispatch({ type: PRODUCT_LIST_REQUEST })

        const { data } = await axios.get('/api/products/')

        dispatch({ type: PRODUCT_LIST_SUCCESS, payload: data })

    } catch (error) {
        dispatch({
            type: PRODUCT_LIST_FAIL,
            payload: error.response && error.response.data.message
                ? error.response.data.message
                : error.message,
        })
    }
}
```

`listProducts` is an **action creator** — a function that returns another function (the thunk pattern). Without `redux-thunk`, Redux only accepts plain objects like `{ type: '...' }`. With thunk, you can dispatch a function, and thunk will call it with `dispatch` so you can dispatch real actions after async work completes.

The three dispatches map directly to the three reducer cases:

| Dispatch | Reducer case | New state |
|---|---|---|
| `PRODUCT_LIST_REQUEST` | `case PRODUCT_LIST_REQUEST` | `{ loading: true, products: [] }` |
| `PRODUCT_LIST_SUCCESS` | `case PRODUCT_LIST_SUCCESS` | `{ loading: false, products: [...] }` |
| `PRODUCT_LIST_FAIL` | `case PRODUCT_LIST_FAIL` | `{ loading: false, error: '...' }` |

#### 4. `Store.jsx` — wiring it all together

```js
import { legacy_createStore as createStore, combineReducers, applyMiddleware } from 'redux'
import { thunk } from 'redux-thunk'
import { composeWithDevTools } from '@redux-devtools/extension'
import { productListReducers } from './reducers/productReducers.js'

const reducer = combineReducers({
    productList: productListReducers,   // more slices added here as app grows
})

const initialState = {}

const middleware = [thunk]

const store = createStore(
    reducer,
    initialState,
    composeWithDevTools(applyMiddleware(...middleware))
)

export default store
```

`combineReducers` merges multiple reducers into one. The key name (`productList`) becomes the key on the store state — so components access it as `state.productList`.

`applyMiddleware(thunk)` — plugs thunk into Redux so async action creators work.

`composeWithDevTools` — connects the Redux DevTools browser extension so you can inspect every action and state change in Chrome DevTools.

`legacy_createStore` — Redux 5 renamed `createStore` to signal it's the "old" API (Redux Toolkit is the modern recommended approach). It works identically — `as createStore` just aliases it so the rest of the code stays the same as the course.

---

### How a component uses the store

Two hooks connect a component to Redux:

```js
const dispatch = useDispatch()    // lets you send actions to the store
const { loading, error, products } = useSelector(state => state.productList)
                                                              ↑
                                            matches the key in combineReducers
```

`useSelector` subscribes the component to that slice of state — whenever `state.productList` changes, the component re-renders automatically.

`useDispatch` gives you the `dispatch` function — you call it with an action or action creator to trigger a state change.

---

### The complete flow — from click to render

```
HomeScreen mounts
    │
    └─ useEffect → dispatch(listProducts())
                            │
                    thunk intercepts (it's a function, not a plain object)
                            │
                    thunk calls: async (dispatch) => { ... }
                            │
                    ①  dispatch({ type: PRODUCT_LIST_REQUEST })
                            │
                        Redux → productListReducers
                            │
                        returns { loading: true, products: [] }
                            │
                        store updates
                            │
                        HomeScreen re-renders → shows loading spinner
                            │
                    ②  await axios.get('/api/products/')  ← hits Django
                            │
                        Django → serializer → JSON response
                            │
                    ③  dispatch({ type: PRODUCT_LIST_SUCCESS, payload: data })
                            │
                        Redux → productListReducers
                            │
                        returns { loading: false, products: [...] }
                            │
                        store updates
                            │
                        HomeScreen re-renders → shows product cards
```

If the axios call fails instead:
```
    ③  dispatch({ type: PRODUCT_LIST_FAIL, payload: error.message })
            │
        returns { loading: false, error: 'Network Error' }
            │
        HomeScreen re-renders → shows error message
```

---

### Package notes — version differences from the course

The course uses older packages incompatible with Redux 5. Here's what changed and why:

| Course code | Your code | Why |
|---|---|---|
| `import thunk from 'redux-thunk'` | `import { thunk } from 'redux-thunk'` | v3 removed default export |
| `from 'redux-devtools-extension'` | `from '@redux-devtools/extension'` | package was renamed/moved |
| `configureStore` from `'redux'` | `legacy_createStore` from `'redux'` | `configureStore` lives in Redux Toolkit, not `redux` |

---

*More sections will be added as the course progresses.*
