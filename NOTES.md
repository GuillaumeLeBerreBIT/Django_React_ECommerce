# ProShop — Django + React E-Commerce (Udemy Course Notes)

> **Course:** [Django with React | An Ecommerce Website](https://www.udemy.com/course/django-with-react-an-ecommerce-website/)
> **Stack:** Django REST Framework (backend) + React SPA (frontend)
> **Purpose:** Personal learning log — concepts, decisions, and code structure explained section by section.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Section 1 — Project Setup & Frontend Scaffold](#section-1--project-setup--frontend-scaffold)
- [Section 2 — Starting the Front End](#section-2--starting-the-front-end)
- [Section 5 — Adding to Shopping Cart](#section-5--adding-to-shopping-cart)
- [Section 6 — Backend User Authentication](#section-6--backend-user-authentication)

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

---

### Product List Reducer & Action (video 21) + Product Details (video 22)

**Files created/updated:**
- `frontend/src/constants/productConstants.js` — six action type constants (list + details)
- `frontend/src/reducers/productReducers.js` — two reducers: `productListReducers`, `productDetailsReducers`
- `frontend/src/actions/productActions.js` — two async action creators: `listProducts`, `listProductDetails`
- `frontend/src/Store.jsx` — registered `productDetailsReducers` in `combineReducers`
- `frontend/src/pages/HomeScreen.jsx` — replaced local `useState`/axios with Redux `useDispatch`/`useSelector`
- `frontend/src/pages/ProductScreen.jsx` — same pattern, wired to `productDetails` slice

---

### Constants — one file per feature, unique strings

```js
// productConstants.js
export const PRODUCT_LIST_REQUEST    = 'PRODUCT_LIST_REQUEST'
export const PRODUCT_LIST_SUCCESS    = 'PRODUCT_LIST_SUCCESS'
export const PRODUCT_LIST_FAIL       = 'PRODUCT_LIST_FAIL'

export const PRODUCT_DETAILS_REQUEST = 'PRODUCT_DETAILS_REQUEST'
export const PRODUCT_DETAILS_SUCCESS = 'PRODUCT_DETAILS_SUCCESS'
export const PRODUCT_DETAILS_FAIL    = 'PRODUCT_DETAILS_FAIL'
```

Each feature (products, cart, user) gets its own constants file with unique strings. Both the action creator and its matching reducer import from the same file — this ensures they always use the identical string, turning typos into import errors rather than silent bugs.

The naming convention `FEATURE_ACTION_STATUS` keeps strings globally unique so two reducers never accidentally react to the same dispatch.

---

### Two reducers — one per feature slice

```js
// productListReducers — handles the product list page
export const productListReducers = (state = { products: [] }, action) => {
    switch (action.type) {
        case PRODUCT_LIST_REQUEST:
            return { loading: true, products: [] }
        case PRODUCT_LIST_SUCCESS:
            return { loading: false, products: action.payload }
        case PRODUCT_LIST_FAIL:
            return { loading: false, error: action.error }
        default:
            return state
    }
}

// productDetailsReducers — handles the single product page
export const productDetailsReducers = (state = { product: { reviews: [] } }, action) => {
    switch (action.type) {
        case PRODUCT_DETAILS_REQUEST:
            return { loading: true, ...state }
        case PRODUCT_DETAILS_SUCCESS:
            return { loading: false, product: action.payload }
        case PRODUCT_DETAILS_FAIL:
            return { loading: false, error: action.error }
        default:
            return state
    }
}
```

**Why two separate reducers instead of one?**
Each reducer owns one slice of state. Keeping them separate means a dispatch to `PRODUCT_LIST_REQUEST` only affects `state.productList` — `state.productDetails` is untouched. If they were merged, fetching the list could accidentally wipe the currently viewed product.

**`...state` in `PRODUCT_DETAILS_REQUEST`:**
```js
case PRODUCT_DETAILS_REQUEST:
    return { loading: true, ...state }
```
The spread `...state` copies the existing `product` into the new state object. This means while a new product is loading, the previous product data stays visible rather than disappearing. `productListReducers` resets `products: []` on request instead — a deliberate difference, since a blank list while refreshing is acceptable.

**Initial state shapes:**

| Reducer | Initial state | Why |
|---|---|---|
| `productListReducers` | `{ products: [] }` | `products.map()` is called on first render — needs an array |
| `productDetailsReducers` | `{ product: { reviews: [] } }` | `product.reviews` may be mapped — needs an array inside |

---

### Two action creators — one per feature

```js
// listProducts — fetches the full product list
export const listProducts = () => async (dispatch) => {
    try {
        dispatch({ type: PRODUCT_LIST_REQUEST })
        const { data } = await axios.get('/api/products/')
        dispatch({ type: PRODUCT_LIST_SUCCESS, payload: data })
    } catch (error) {
        dispatch({
            type: PRODUCT_LIST_FAIL,
            error: error.response && error.response.data.message
                ? error.response.data.message
                : error.message,
        })
    }
}

// listProductDetails — fetches a single product by id
export const listProductDetails = (id) => async (dispatch) => {
    try {
        dispatch({ type: PRODUCT_DETAILS_REQUEST })
        const { data } = await axios.get(`/api/products/${id}`)
        dispatch({ type: PRODUCT_DETAILS_SUCCESS, payload: data })
    } catch (error) {
        dispatch({
            type: PRODUCT_DETAILS_FAIL,
            error: error.response && error.response.data.message
                ? error.response.data.message
                : error.message,
        })
    }
}
```

`listProducts` takes no arguments — it always fetches all products.
`listProductDetails` takes `id` — passed in from `useParams()` in the component, then interpolated into the URL.

**The error message pattern:**
```js
error.response && error.response.data.message
    ? error.response.data.message   // Django sent a structured error message
    : error.message                 // fallback: generic JS error (e.g. 'Network Error')
```
Django REST Framework returns errors as `{ message: '...' }` in the response body. If that exists, use it. Otherwise fall back to the raw JS error message.

---

### Store — registering both reducers

```js
const reducer = combineReducers({
    productList:    productListReducers,     // state.productList
    productDetails: productDetailsReducers,  // state.productDetails
})

const initialState = {
    productList: { products: [] }   // prevents .map() crash before first fetch
}
```

`initialState` in `createStore` overrides reducer defaults for the matching slice. `productList` needs an explicit `{ products: [] }` here because otherwise the store starts with `{}` and `products` is `undefined` on the first render — crashing `.map()`.

`productDetails` doesn't need an entry in `initialState` because its default `{ product: { reviews: [] } }` is safe to render with before any fetch completes.

---

### Connecting components to the store

**HomeScreen — reading `state.productList`:**

```js
const dispatch = useDispatch()
const productList = useSelector((state) => state.productList)
const { loading, error, products } = productList

useEffect(() => {
    dispatch(listProducts())
}, [dispatch])
```

**ProductScreen — reading `state.productDetails`:**

```js
const { id } = useParams()
const dispatch = useDispatch()
const productDetails = useSelector((state) => state.productDetails)
const { loading, error, product } = productDetails

useEffect(() => {
    dispatch(listProductDetails(id))
}, [id, dispatch])
```

**`useSelector`** — subscribes the component to a slice of the store. The selector function `(state) => state.productList` picks exactly what this component needs. When that slice changes, React re-renders the component automatically.

**`useDispatch`** — gives you the `dispatch` function. You call it with an action creator to trigger the async flow.

**`useParams`** — from React Router, reads the `:id` from the URL (e.g. `/product/3` → `id = '3'`). Passed into `listProductDetails(id)` so the correct product is fetched.

---

### Loading/error guard pattern

Both screens use the same three-state ternary to handle the async lifecycle:

```jsx
{loading ? (
    <Loader />                              // fetch in progress
) : error ? (
    <Message variant="danger">{error}</Message>  // fetch failed
) : (
    <Row>...</Row>                          // fetch succeeded, render data
)}
```

This is essential because on the very first render — before the `useEffect` dispatch has even fired — `product` is the initial state default `{ reviews: [] }`. Without the guard, JSX would try `product.image` on an object that has no `image` field, crashing with `Cannot read properties of undefined`.

The guard ensures the JSX that accesses product fields only runs in the third branch, after `PRODUCT_DETAILS_SUCCESS` has set a real product into the store.

---

### How dispatch knows which reducer to call — summary

Redux broadcasts every dispatched action to **all** registered reducers. Each reducer uses its `switch` statement to decide if the action is relevant to it:

```
dispatch({ type: 'PRODUCT_LIST_REQUEST' })
    │
    ├──► productListReducers   → case matches → returns { loading: true, products: [] }
    └──► productDetailsReducers → no match   → default → returns state unchanged
```

This is why unique constant strings matter — if two reducers shared the same string, both would react to the same dispatch, corrupting unrelated state.

---

---

## Section 5 — Adding to Shopping Cart

### What was built

A fully functional cart system: add items, change quantity, remove items, and persist the cart across page refreshes via `localStorage`.

**Files created:**
- `frontend/src/constants/cartConstants.js` — `CART_ADD_ITEM` and `CART_REMOVE_ITEM` action type strings
- `frontend/src/actions/cartActions.js` — two async action creators: `addToCart`, `removeFromCart`
- `frontend/src/reducers/cartReducers.js` — `cartReducer` handling add and remove
- `frontend/src/pages/CartScreen.jsx` — the cart page UI

**Files updated:**
- `frontend/src/Store.jsx` — registered `cartReducer` in `combineReducers`; hydrates cart from `localStorage` on startup
- `frontend/src/pages/ProductScreen.jsx` — added qty dropdown and "Add to Cart" button that dispatches `addToCart`

---

### cartConstants.js — action type strings

```js
export const CART_ADD_ITEM    = 'CART_ADD_ITEM'
export const CART_REMOVE_ITEM = 'CART_REMOVE_ITEM'
```

Same pattern as product constants — shared strings imported by both the action creator and the reducer so a typo becomes an import error, not a silent bug.

---

### cartActions.js — two action creators

```js
export const addToCart = (id, qty) => async (dispatch, getState) => {
    const { data } = await axios.get(`/api/products/${id}`)

    dispatch({
        type: CART_ADD_ITEM,
        payload: {
            product: data._id,
            name: data.name,
            image: data.image,
            price: data.price,
            countInStock: data.countInStock,
            qty
        }
    })

    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))
}

export const removeFromCart = (id) => (dispatch, getState) => {
    dispatch({ type: CART_REMOVE_ITEM, payload: id })
    localStorage.setItem('cartItems', JSON.stringify(getState().cart.cartItems))
}
```

**Key points:**

- `addToCart` is `async` because it fetches the product from the API first — it builds the cart item from live data, not from whatever the component already has
- `removeFromCart` is NOT async — no API call needed, it just dispatches the id to remove
- Both call `getState().cart.cartItems` **after** dispatching — the dispatch has already updated the store, so `getState()` returns the new state, which is what gets saved to `localStorage`
- `dispatch` and `getState` are **injected by Redux thunk** — you never pass them yourself; thunk intercepts the returned function and calls it with those two arguments automatically

**Why `getState()` after dispatch gives updated state:**
```
dispatch(CART_ADD_ITEM)
    → Redux calls cartReducer
        → reducer returns new state
            → store updates
                → getState() now reflects that new state
                    → localStorage.setItem(...)  ← saves the updated cart
```

---

### cartReducers.js — add and remove logic

```js
export const cartReducer = (state = { cartItems: [] }, action) => {
  switch (action.type) {

    case CART_ADD_ITEM:
      const item = action.payload;
      const existItem = state.cartItems.find((x) => x.product === item.product);

      if (existItem) {
        // product already in cart — replace the whole item (qty is baked in)
        return {
          ...state,
          cartItems: state.cartItems.map((x) =>
            x.product === existItem.product ? item : x
          ),
        };
      } else {
        // new product — append it
        return {
          ...state,
          cartItems: [...state.cartItems, item],
        };
      }

    case CART_REMOVE_ITEM:
      return {
        ...state,
        cartItems: state.cartItems.filter((i) => i.product !== action.payload)
      }

    default:
      return state;
  }
};
```

**Add logic:**
The reducer asks "is this product already in the cart?" using `.find()`. If yes, it **replaces** the whole item (not just increments) — the correct qty was already calculated before dispatch. If no, it appends.

**Remove logic:**
`.filter()` returns a new array excluding the item whose `product` id matches the payload. Redux state must never be mutated — filter creates a new array instead of splicing the old one.

**Why replace instead of increment:**
The qty is set by the user in the dropdown on `ProductScreen` before they click Add to Cart. By the time the reducer sees the item, the payload already contains `qty: 3` (or whatever they chose). The reducer just decides *where* to put it.

---

### Store.jsx — cart slice and localStorage hydration

```js
const cartItemsFromStorage = localStorage.getItem('cartItems')
    ? JSON.parse(localStorage.getItem('cartItems'))
    : []

const initialState = {
    productList: { products: [] },
    cart: { cartItems: cartItemsFromStorage }  // pre-populate from localStorage
}

const reducer = combineReducers({
    productList:    productListReducers,
    productDetails: productDetailsReducers,
    cart:           cartReducer               // new slice
})
```

On every page load, the store checks `localStorage` for saved cart items. If they exist, they become the initial state — the cart persists across browser refreshes.

**localStorage vs Redux state:**
| | Redux store | localStorage |
|---|---|---|
| Lives in | Browser memory (RAM) | Browser disk |
| Survives refresh | No | Yes |
| Updated | On every dispatch | Manually after dispatch |

---

### CartScreen.jsx — the cart page

```jsx
export default function CartScreen() {
  const { id } = useParams()
  const [searchParams] = useSearchParams()
  const qty = Number(searchParams.get('qty')) || 1

  const dispatch = useDispatch()
  const { cartItems } = useSelector(state => state.cart)

  useEffect(() => {
    if (id) {
      dispatch(addToCart(id, qty))  // runs when navigating to /cart/:id?qty=N
    }
  }, [dispatch, id, qty])

  function removeFromCartHandler(id) {
    dispatch(removeFromCart(id))
  }

  return (
    <Row>
      <Col md={8}>
        {/* cart items list */}
        <ListGroup>
          {cartItems.map(item => (
            <ListGroup.Item key={item.product}>
              <Row>
                <Col md={2}><Image src={item.image} fluid rounded /></Col>
                <Col md={3}><Link to={`/product/${item.product}`}>{item.name}</Link></Col>
                <Col md={2}>${item.price}</Col>
                <Col md={3}>
                  {/* qty dropdown — dispatches addToCart with new qty on change */}
                  <Form.Control as="select" value={item.qty}
                    onChange={(e) => dispatch(addToCart(item.product, Number(e.target.value)))}>
                    {[...Array(item.countInStock).keys()].map((x) => (
                      <option key={x + 1} value={x + 1}>{x + 1}</option>
                    ))}
                  </Form.Control>
                </Col>
                <Col md={1}>
                  <Button variant="light" onClick={() => removeFromCartHandler(item.product)}>
                    <i className="fas fa-trash"></i>
                  </Button>
                </Col>
              </Row>
            </ListGroup.Item>
          ))}
        </ListGroup>
      </Col>

      <Col md={4}>
        <Card>
          <ListGroup variant="flush">
            <ListGroup.Item>
              <h2>Subtotal ({cartItems.reduce((acc, item) => acc + item.qty, 0)})</h2>
              ${cartItems.reduce((acc, item) => acc + item.price * item.qty, 0).toFixed(2)}
            </ListGroup.Item>
            <ListGroup.Item>
              <Button disabled={cartItems.length === 0}>Proceed to Checkout</Button>
            </ListGroup.Item>
          </ListGroup>
        </Card>
      </Col>
    </Row>
  )
}
```

**The qty dropdown trick:**
```js
[...Array(item.countInStock).keys()].map((x) => (
  <option key={x + 1} value={x + 1}>{x + 1}</option>
))
```
`Array(10)` creates 10 empty slots — `.map()` skips empty slots. `.keys()` returns the indices `[0..9]` as an iterator, spread into a real array. Then `x + 1` shifts from 0-based to 1-based so options show 1 through 10.

**The subtotal with `.reduce()`:**
```js
cartItems.reduce((acc, item) => acc + item.qty, 0)        // total item count
cartItems.reduce((acc, item) => acc + item.price * item.qty, 0).toFixed(2)  // total price
```
`.reduce()` accumulates a running total across all items. `acc` starts at `0`, each iteration adds the current item's contribution.

---

### React Router v5 → v6 differences encountered this section

| Feature | v5 (course) | v6 (what you used) |
|---|---|---|
| Navigate programmatically | `history.push('/path')` prop | `const navigate = useNavigate()` → `navigate('/path')` |
| Read query string | `location.search` prop | `const [searchParams] = useSearchParams()` → `searchParams.get('qty')` |
| Go back | `history.goBack()` | `navigate(-1)` |

---

### The full cart data flow

```
User clicks "Add to Cart" on ProductScreen
    ↓
addToCartHandler() → navigate(`/cart/${id}?qty=${qty}`)
    ↓
CartScreen mounts with id and qty from URL
    ↓
useEffect → dispatch(addToCart(id, qty))
    ↓
addToCart fetches product from Django API
    ↓
dispatch({ type: CART_ADD_ITEM, payload: { ...productData, qty } })
    ↓
cartReducer: item exists? replace : append
    ↓
getState().cart.cartItems → save to localStorage
    ↓
CartScreen re-renders with updated cartItems
```

---

### Key Concepts from this Section

**Thunk injects `dispatch` and `getState` automatically**
When you return a function from an action creator, Redux thunk intercepts it and calls it with `(dispatch, getState)`. You never pass those yourself — thunk handles it because it's registered as middleware.

**State immutability**
Redux reducers must never mutate existing state. Always return a new object/array:
- Add item: `[...state.cartItems, item]` — new array
- Replace item: `.map()` — new array
- Remove item: `.filter()` — new array

**`getState()` order matters**
Calling `getState()` after `dispatch()` gives you the **already-updated** state. The reducer runs synchronously during dispatch, so by the time the next line executes, the store reflects the change.

**localStorage as a persistence layer**
Redux resets on page refresh. `localStorage` survives it. The pattern here:
1. After every cart change, serialize cart to `localStorage`
2. On store init, read `localStorage` → set as `initialState`

This two-way sync is manual — you maintain it yourself (no automatic Redux-localStorage binding).

---

---

## Section 6 — Backend User Authentication

### What was built

A complete JWT-based authentication system on the Django backend: login endpoint, protected routes, user profile, and admin-only routes.

**Files created/updated:**
- `backend/api/serializers.py` — `UserSerializer`, `UserSerializerWithToken` (extends UserSerializer with a JWT access token)
- `backend/api/views.py` — `MyTokenObtainPairSerializer`, `MyTokenObtainPairView`, `GetUserProfile`, `GetUsers`
- `backend/api/urls.py` — new routes for login, profile, and user list
- `backend/backend/settings.py` — `REST_FRAMEWORK` default auth class + `SIMPLE_JWT` config

---

### Why JWT instead of sessions

Django's default authentication uses **sessions** — the server stores a session record and sends a cookie to the browser. This works for traditional server-rendered apps but has problems for a React SPA:

| Sessions | JWT |
|---|---|
| State stored on the server | Stateless — all data is in the token |
| Tied to cookies | Sent as a header (`Authorization: Bearer <token>`) |
| Doesn't work well across origins | Works across any client (React, mobile, etc.) |
| Hard to scale horizontally | No server-side state to sync |

JWT (JSON Web Token) is a signed string the server issues on login. The client stores it and sends it with every request. The server verifies the signature without touching a database.

```
Login → server issues token → client stores it
Every request → client sends token in header → server verifies signature → grants/denies access
```

---

### settings.py — JWT configuration

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
```

**`DEFAULT_AUTHENTICATION_CLASSES`** — tells DRF to look for a JWT token in the `Authorization` header on every request, instead of checking for a session cookie.

**`ACCESS_TOKEN_LIFETIME: timedelta(days=30)`** — access tokens expire after 30 days. In production you'd set this much shorter (minutes/hours) and use refresh tokens to get new ones. 30 days is convenient for development.

**`ALGORITHM: "HS256"`** — the signing algorithm. HS256 is symmetric (same key signs and verifies). The token is signed with `SECRET_KEY` from Django's settings — keep that secret in production.

**`AUTH_HEADER_TYPES: ("Bearer",)`** — the token must be sent as:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

### serializers.py — UserSerializer and UserSerializerWithToken

```python
class UserSerializer(serializers.ModelSerializer):
    name    = serializers.SerializerMethodField(read_only=True)
    _id     = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name
```

**`SerializerMethodField`** — a computed field backed by a method instead of a model column. DRF automatically calls `get_<fieldname>` to get the value:

| Field name | Method called |
|---|---|
| `name` | `get_name()` |
| `_id` | `get__id()` (double underscore — field name starts with `_`) |
| `isAdmin` | `get_isAdmin()` |

**Why use methods instead of direct model fields:**
- `_id` — Django's User model uses `id`, but the frontend expects `_id` (MongoDB-style convention from earlier). The method renames it.
- `isAdmin` — Django uses `is_staff` (snake_case). The method renames it to camelCase for React.
- `name` — `first_name` might be empty. The method falls back to `email` if it is.

**`obj` in each method** — the actual `User` instance being serialized. `Meta` is the blueprint (config), `obj` is the live data.

---

### UserSerializerWithToken — adding the JWT to the response

```python
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
```

Extends `UserSerializer` — inherits all the same fields and methods, just adds `token` on top.

`RefreshToken.for_user(obj)` — simplejwt generates a refresh token for this user. `.access_token` derives the access token from it. `str(...)` converts the token object to the JWT string (`eyJ...`).

**Why two serializers:**
- `UserSerializer` — used when you just need user data (profile page, user list)
- `UserSerializerWithToken` — used only on login, where the client also needs the token to store

---

### views.py — custom login serializer and view

```python
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)          # simplejwt validates credentials
                                                # and sets self.user

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v                         # merge user data into token response

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
```

**Why subclass instead of using simplejwt directly:**
By default, simplejwt's login endpoint only returns `{ access, refresh }` tokens. The React frontend also needs user info (name, email, isAdmin) immediately after login — without a second request. Subclassing lets you inject that data into the login response.

**How `self.user` gets populated:**
`super().validate(attrs)` calls simplejwt's parent implementation which:
1. Calls Django's `authenticate(username, password)`
2. Django's `ModelBackend` queries `auth_user` table and checks the hashed password
3. If valid, sets `self.user = User instance`

By the time your code runs after `super()`, `self.user` is already populated.

**The merge loop:**
```python
for k, v in serializer.items():
    data[k] = v
```
`data` starts as `{ access: '...', refresh: '...' }` from simplejwt. This loop adds `_id`, `username`, `email`, `name`, `isAdmin`, `token` — so the final response includes everything the frontend needs in one call.

---

### views.py — protected routes

```python
class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]   # ← requires valid JWT token

    def get(self, request):
        user = request.user                  # ← simplejwt populates this from the token
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class GetUsers(APIView):
    permission_classes = [IsAdminUser]       # ← requires is_staff = True

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
```

**`permission_classes`** — DRF's way to protect a view. Evaluated before the method body runs. If the check fails, DRF returns a `403 JSON response` — not a redirect (which would be useless for React).

| Permission class | Allows |
|---|---|
| `IsAuthenticated` | Any user with a valid JWT |
| `IsAdminUser` | Only users where `is_staff = True` |
| `AllowAny` | Everyone, no token needed (default) |

**`request.user`** — when a valid JWT is in the `Authorization` header, simplejwt's authentication class decodes it and sets `request.user` to the matching `User` instance automatically. No database lookup code needed in the view.

**Plain Django equivalent:**
```python
# Plain Django — redirects to login page (bad for APIs)
@login_required
def my_view(request): ...

# DRF — returns 403 JSON (correct for APIs)
class MyView(APIView):
    permission_classes = [IsAuthenticated]
```

---

### urls.py — new routes

```python
urlpatterns = [
    path('users/login/',   views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/profile/', views.GetUserProfile.as_view(),        name='get_user_profile'),
    path('users/',         views.GetUsers.as_view(),              name='get_users'),
    # ... existing product routes
]
```

| Endpoint | Method | Auth required | Returns |
|---|---|---|---|
| `/api/users/login/` | POST | None | `{ access, refresh, _id, username, email, name, isAdmin, token }` |
| `/api/users/profile/` | GET | Any authenticated user | User profile data |
| `/api/users/` | GET | Admin only | All users |

---

### Serializer direction — outgoing vs incoming

Serializers work in **both directions** — not just for sending data out:

```python
# Outgoing (DB → JSON) — no data= kwarg
serializer = UserSerializer(user_instance)
return Response(serializer.data)

# Incoming (JSON → DB) — data= kwarg signals incoming
serializer = UserSerializer(data=request.data)
if serializer.is_valid():       # validates format, required fields, types
    serializer.save()           # writes to DB
else:
    return Response(serializer.errors, status=400)
```

The serializer acts as a **two-way gatekeeper**:
- **Outgoing:** converts Python objects to JSON-serializable dicts
- **Incoming:** validates and cleans user-submitted data before it touches the database

---

### How Django's authenticate() works under the hood

```python
# Django's authenticate() — simplified
def authenticate(request=None, **credentials):
    for backend in registered_backends:
        user = backend.authenticate(request, **credentials)
        if user is None:
            continue
        user.backend = backend_path
        return user
    # no backend matched → fire login_failed signal
```

Django supports multiple authentication backends (e.g. username+password AND OAuth). `authenticate()` loops through all of them, returns the first `User` it gets back.

The default backend is `ModelBackend`:
```python
# ModelBackend (simplified)
def authenticate(self, request, username=None, password=None):
    user = User.objects.get(username=username)   # DB lookup
    if user.check_password(password):            # bcrypt hash check
        return user
    return None
```

**Full login chain:**
```
POST /api/users/login/ { username, password }
        ↓
MyTokenObtainPairView → MyTokenObtainPairSerializer.validate()
        ↓
super().validate() → simplejwt → Django authenticate()
        ↓
ModelBackend → User.objects.get() → check_password()
        ↓
self.user = User instance
        ↓
UserSerializerWithToken(self.user) → generates JWT + user data
        ↓
Response: { access, refresh, _id, username, email, name, isAdmin, token }
        ↓
React stores token → sends it in Authorization header on future requests
        ↓
simplejwt decodes token → sets request.user automatically
```

---

### Key Concepts from this Section

**JWT (JSON Web Token)**
A signed string containing encoded user data. The server signs it with a secret key on login; any future request can be verified by checking the signature — no database lookup needed. Three parts: `header.payload.signature`, all base64-encoded.

**`SerializerMethodField`**
Lets you define a computed field backed by a Python method (`get_<fieldname>`). Used when the value needs logic (renaming, fallbacks, generating tokens) rather than just reading a model column directly.

**`self.user` in simplejwt**
Set automatically by `TokenObtainPairSerializer`'s `validate()` after credentials are verified. Not a DRF convention — specific to simplejwt. Always call `super().validate()` first or `self.user` won't exist.

**`permission_classes`**
DRF's access control system. Evaluated before any view logic runs. Returns `403 JSON` on failure — never a redirect. Use `IsAuthenticated` for logged-in users, `IsAdminUser` for staff only, `AllowAny` for public endpoints.

**`request.user`**
When a valid JWT is in the `Authorization: Bearer <token>` header, DRF's JWT authentication class decodes it and populates `request.user` with the `User` instance — automatically, with no code needed in the view.

---

*More sections will be added as the course progresses.*
