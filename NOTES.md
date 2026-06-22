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
- [Section 7 — User Login Reducer & Action](#section-7--user-login-reducer--action)
- [Section 8 — Checkout Flow (Cart → Login → Shipping → Payment → Place Order)](#section-8--checkout-flow-cart--login--shipping)
- [Section 9 — Get Order by ID API](#section-9--get-order-by-id-api)
- [Section 11 — Admin Screen Part 2 (Products & Orders CRUD)](#section-11--admin-screen-part-2-products--orders-crud)

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

### User Registration — registerUser view

```python
class registerUser(APIView):

    def post(self, request):
        try:
            data = request.data

            user = User.objects.create(
                first_name=data['name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password']),
            )

            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except:
            message = {'detail': 'User with this email already exists'}
            return Response(message, status.HTTP_400_BAD_REQUEST)
```

**Key points:**

**`make_password()`** — never store passwords as plain text. `make_password()` from `django.contrib.auth.hashers` runs the password through Django's hashing algorithm (bcrypt by default) before saving. If you used `User.objects.create()` without it, the raw password would be stored in the database — a serious security hole.

```python
# Wrong — stores plain text
User.objects.create(password=data['password'])

# Correct — stores a bcrypt hash
User.objects.create(password=make_password(data['password']))
```

**`username=data['email']`** — Django's `User` model requires a unique `username`. Since this app uses email-based login (not a separate username), both `username` and `email` are set to the same value. The `signals.py` file (see below) enforces this automatically going forward.

**`UserSerializerWithToken` on registration** — after creating the user, the response includes the JWT token immediately. This means the frontend can log the user in straight after registration without a second login request.

**`try/except` for duplicate emails** — `User.objects.create()` raises an `IntegrityError` if a user with that email/username already exists (database unique constraint). The bare `except` catches it and returns a readable error message with HTTP 400.

---

### signals.py — keeping username in sync with email

```python
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != '':
        user.username = user.email

pre_save.connect(updateUser, sender=User)
```

**What a Django signal is:**
A signal is a hook that fires automatically when something happens in Django — before/after a model is saved, before/after it's deleted, etc. You subscribe a function to a signal and Django calls it at the right moment.

```
User.save() called
    ↓
Django fires pre_save signal
    ↓
updateUser() runs → sets username = email
    ↓
Django writes to database with updated username
```

**Why `pre_save` and not `post_save`:**
`pre_save` fires **before** the record hits the database — so you can still modify `instance` and those changes get saved. `post_save` fires after — too late to modify the record being saved.

**Why this signal exists:**
Django's `User` model is built around `username` as the login identifier. But this app uses email for login. Without the signal, if a user updates their email via the profile page, their `username` would stay as the old email — breaking login. The signal keeps them in sync automatically on every save.

| Event | Signal |
|---|---|
| Before save | `pre_save` |
| After save | `post_save` |
| Before delete | `pre_delete` |
| After delete | `post_delete` |

**`sender=User`** — limits the signal to only fire when a `User` model is saved, not every model in the entire app.

**`instance`** — the actual `User` object about to be saved. Mutating `instance` here directly changes what gets written to the database.

---

### apps.py — registering signals

```python
class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        import api.signals
```

Django signals aren't loaded automatically — you have to import the signals file somewhere that runs on startup. `AppConfig.ready()` is Django's designated hook for startup code. It runs once when the app is fully loaded.

Without this, `signals.py` would sit there doing nothing — the `pre_save` connection would never be registered and `updateUser` would never fire.

**Why not just import signals at the top of `views.py`?**
`views.py` is only imported when a request hits a view — not guaranteed to run at startup. `ready()` always runs at startup, making it the correct place.

---

### New URL route

```python
path('users/register/', views.registerUser.as_view(), name='register'),
```

| Endpoint | Method | Auth | Body | Returns |
|---|---|---|---|---|
| `/api/users/register/` | POST | None | `{ name, email, password }` | User data + JWT token |

---

### Registration vs Login flow comparison

```
REGISTRATION                          LOGIN
─────────────────────────────         ─────────────────────────────
POST /api/users/register/             POST /api/users/login/
  { name, email, password }             { username (=email), password }
        ↓                                     ↓
User.objects.create(...)              authenticate(username, password)
make_password(password)               ModelBackend → DB lookup
        ↓                                     ↓
User saved to database                self.user = User instance
        ↓                                     ↓
UserSerializerWithToken(user)         UserSerializerWithToken(self.user)
        ↓                                     ↓
Response: user data + token           Response: user data + token
```

Both return the same shape — the React frontend handles both the same way (stores the token, redirects the user).

---

### Refactoring — splitting views.py and urls.py into folders

As the app grows, keeping all views in one `views.py` and all URLs in one `urls.py` becomes hard to navigate. The solution is to convert each into a **package** (a folder with an `__init__.py`) and split by feature.

**Before:**
```
api/
├── views.py        ← all views in one file
└── urls.py         ← all urls in one file
```

**After:**
```
api/
├── views/
│   ├── __init__.py       ← makes views/ a Python package
│   ├── user_views.py     ← login, register, profile, users list
│   └── product_views.py  ← product list, single product
├── urls/
│   ├── user_urls.py      ← /api/users/* routes
│   ├── product_urls.py   ← /api/products/* routes
│   └── order_urls.py     ← /api/orders/* routes (future)
└── _urls.py              ← old urls.py kept as reference (underscore = inactive)
```

**Why `__init__.py` is required:**
Python only treats a folder as an importable package if it contains `__init__.py`. Without it, `from api.views import user_views` fails with `ImportError` because Python finds the old `views.py` file first, or doesn't recognise the folder at all.

```
Without __init__.py:
  from api.views import user_views  →  ImportError: cannot import name 'user_views' from 'api.views'

With __init__.py:
  from api.views import user_views  →  ✓ imports api/views/user_views.py
```

**Gotcha — `views.py` and `views/` can't coexist:**
If both `views.py` and `views/` exist, Python always picks the file (`views.py`) over the folder. The old `views.py` must be deleted (or renamed) for the package to be used. This was the cause of the `ImportError` encountered during refactoring.

---

### views/ — imports use `..` for relative paths

Inside `views/user_views.py`, imports that used to be `from .models import ...` now need an extra dot because the file is one level deeper:

```python
# Before (views.py at api/ level)
from .models import Product
from .serializers import UserSerializer

# After (user_views.py inside api/views/)
from ..models import Product        # .. = go up one level to api/
from ..serializers import UserSerializer
```

`..` means "parent package" — it navigates up from `api/views/` to `api/` where `models.py` and `serializers.py` live.

---

### urls/ — feature-based URL files

Each URL file handles one feature prefix and imports only its relevant views module:

**`user_urls.py`:**
```python
from api.views import user_views as views

urlpatterns = [
    path('login/',   views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerUser.as_view(),         name='register'),
    path('profile/', views.GetUserProfile.as_view(),        name='get_user_profile'),
    path('',         views.GetUsers.as_view(),              name='get_users'),
]
```

**`product_urls.py`:**
```python
from api.views import product_views as views

urlpatterns = [
    path('',         views.GetProducts.as_view(), name='get_products'),
    path('<str:pk>', views.GetProduct.as_view(),  name='get_product'),
]
```

Notice the paths here are **short** — no `users/` or `products/` prefix. The prefix is added in the project-level `urls.py` via `include()`.

---

### backend/urls.py — project-level router updated

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('api.urls.product_urls')),
    path('api/users/',    include('api.urls.user_urls')),
    path('api/orders/',   include('api.urls.order_urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

The old single `include('api.urls')` is replaced by three separate includes, one per feature. Each `include()` points to a dotted Python path to the URL module.

**How the full URL is assembled:**

```
backend/urls.py prefix    +    feature urls.py path    =    full URL
─────────────────────────────────────────────────────────────────────
'api/users/'              +    'login/'                =    /api/users/login/
'api/users/'              +    'register/'             =    /api/users/register/
'api/users/'              +    'profile/'              =    /api/users/profile/
'api/users/'              +    ''                      =    /api/users/
'api/products/'           +    ''                      =    /api/products/
'api/products/'           +    '<str:pk>'              =    /api/products/<pk>
```

**`static()` line:**
```python
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
Tells Django to serve uploaded media files (product images) during development. In production a web server like Nginx handles this instead.

---

### Final backend structure at end of Section 6

```
backend/
├── manage.py
├── backend/                        ← Django project config
│   ├── settings.py                 ← JWT config, installed apps, CORS, media
│   └── urls.py                     ← top-level router (admin + api/* includes)
└── api/                            ← Django app
    ├── apps.py                     ← registers signals on startup via ready()
    ├── models.py                   ← Product, Order, Review, etc.
    ├── serializers.py              ← UserSerializer, UserSerializerWithToken, ProductSerializer
    ├── signals.py                  ← pre_save: keeps username in sync with email
    ├── admin.py                    ← registers models in Django admin panel
    ├── views/
    │   ├── __init__.py
    │   ├── user_views.py           ← login, register, profile, users list
    │   └── product_views.py        ← product list, single product
    └── urls/
        ├── user_urls.py            ← /api/users/* routes
        ├── product_urls.py         ← /api/products/* routes
        └── order_urls.py           ← /api/orders/* routes (placeholder)
```

---

---

---

## Section 7 — User Login Reducer & Action (Frontend)

### What was built

The frontend Redux layer for user authentication: constants, a reducer, an async action creator, and the store updated to persist login state across page refreshes.

**Files created:**
- `frontend/src/constants/userConstants.js` — four action type strings for login
- `frontend/src/reducers/userReducers.js` — `userLoginReducers` handling the login lifecycle
- `frontend/src/actions/userActions.js` — `login` async action creator, also handles logout

**Files updated:**
- `frontend/src/Store.jsx` — registered `userLoginReducers` in `combineReducers`; hydrates login state from `localStorage` on startup

---

### userConstants.js — four action type strings

```js
export const USER_LOGIN_REQUEST = 'USER_LOGIN_REQUEST'
export const USER_LOGIN_SUCCESS = 'USER_LOGIN_SUCCESS'
export const USER_LOGIN_FAIL    = 'USER_LOGIN_FAIL'
export const USER_LOGOUT        = 'USER_LOGOUT'
```

Same pattern as products and cart — one constants file per feature, shared by both the action creator and the reducer. `USER_LOGOUT` is included here even though the reducer handles it passively (wiping state) and no API call is needed for it.

---

### userReducers.js — the login state machine

```js
export const userLoginReducers = (state = {}, action) => {
  switch (action.type) {
    case USER_LOGIN_REQUEST:
      return { loading: true }
    case USER_LOGIN_SUCCESS:
      return { loading: false, userInfo: action.payload }
    case USER_LOGIN_FAIL:
      return { loading: false, error: action.error }
    case USER_LOGOUT:
      return {}
    default:
      return state
  }
}
```

**State shape at each stage:**

| Action dispatched | New `state.userLogin` |
|---|---|
| `USER_LOGIN_REQUEST` | `{ loading: true }` |
| `USER_LOGIN_SUCCESS` | `{ loading: false, userInfo: { name, email, token, isAdmin, ... } }` |
| `USER_LOGIN_FAIL` | `{ loading: false, error: "Invalid credentials" }` |
| `USER_LOGOUT` | `{}` — completely empty, userInfo wiped |

**Why each case replaces the whole object (not spreads):**
On `SUCCESS`, you don't want a stale `error` key from a previous failed attempt to linger. On `LOGOUT`, you want a guaranteed clean slate. Returning a fresh object is safer than `{ ...state, ... }` here.

**Initial state is `{}`:**
Unlike `productListReducers` which starts with `{ products: [] }` to prevent a crash on `.map()`, the login reducer's initial state can safely be empty — no component tries to `.map()` over `userInfo`.

---

### userActions.js — the login action creator

```js
export const login = (email, password) => async (dispatch) => {
  try {
    dispatch({ type: USER_LOGIN_REQUEST })

    const config = {
      headers: { 'Content-type': 'application/json' }
    }

    const { data } = await axios.post(
      '/api/users/login/',
      { username: email, password: password },
      config
    )

    dispatch({ type: USER_LOGIN_SUCCESS, payload: data })

    localStorage.setItem('userInfo', JSON.stringify(data))

  } catch (error) {
    dispatch({
      type: USER_LOGIN_FAIL,
      error: error.response && error.response.data.detail
        ? error.response.data.detail
        : error.message,
    })
  }
}
```

**Step by step:**

```
dispatch(login(email, password))
    ↓
thunk intercepts → calls async (dispatch) => { ... }
    ↓
① dispatch USER_LOGIN_REQUEST
   → state.userLogin = { loading: true }
   → UI shows spinner
    ↓
② axios.post('/api/users/login/', { username: email, password })
   → hits Django's MyTokenObtainPairView
    ↓
③a Django validates credentials → returns { _id, name, email, isAdmin, token, ... }
   → dispatch USER_LOGIN_SUCCESS, payload: data
   → state.userLogin = { loading: false, userInfo: { ... } }
   → localStorage.setItem('userInfo', JSON.stringify(data))
   → UI shows logged-in header
    ↓
③b Django returns 401
   → dispatch USER_LOGIN_FAIL, error: "No active account..."
   → state.userLogin = { loading: false, error: "..." }
   → UI shows error message
```

**Why `username: email` in the POST body:**
Django's default auth system authenticates with a field called `username`, even though this app collects email in the UI. The `signals.py` file on the backend keeps `username` and `email` in sync. So we send the email value under the `username` key to satisfy Django's expected field name.

**Why the `Content-type` header:**
Django REST Framework needs to know the body is JSON, not a form submission. Without this header, `request.data` on the Django side would be empty.

**The error field key is `error`, not `payload`:**
Note that `USER_LOGIN_FAIL` dispatches `error: ...` (not `payload: ...`). The reducer reads it as `action.error`. This is an inconsistency with how the product reducers work (they also use `action.error`) — just be consistent within your own project.

**`localStorage.setItem` — no `getState()` needed here:**
Unlike the cart action which called `getState()` to read the updated store, the login action already has `data` in scope (the raw axios response). It saves that directly, skipping the extra store read.

---

### Store.jsx — two additions

**1. `userLogin` registered in `combineReducers`:**

```js
const reducer = combineReducers({
    productList:    productListReducers,
    productDetails: productDetailsReducers,
    cart:           cartReducer,
    userLogin:      userLoginReducers    // ← NEW
})
```

The key `userLogin` is what components use in `useSelector(state => state.userLogin)`.

**2. `userInfo` hydrated from `localStorage` on startup:**

```js
const userInfoFromStorage = localStorage.getItem('userInfo')
    ? JSON.parse(localStorage.getItem('userInfo'))
    : null

const initialState = {
    productList: { products: [] },
    cart:        { cartItems: cartItemsFromStorage },
    userLogin:   { userInfo: userInfoFromStorage }   // ← NEW
}
```

On every page load, Redux checks `localStorage` for a previously saved `userInfo`. If it exists, the store starts with the user already logged in — so the nav bar shows their name and login persists across browser refreshes.

**Full localStorage strategy in this app:**

| What's persisted | Key in localStorage | When saved | When read |
|---|---|---|---|
| Cart items | `cartItems` | After every cart dispatch | Store init |
| User info + token | `userInfo` | After successful login | Store init |

---

### `useEffect` — the hook that triggers async work after render

`useEffect` runs code **after** the component renders, and only when the values in its dependency array have changed. It's the correct place for side effects like API calls and Redux dispatches.

```js
useEffect(() => {
    // code to run
}, [dependency1, dependency2])
```

| Dependency array | When it runs |
|---|---|
| No array | Every render (almost never what you want) |
| `[]` | Once, when the component first mounts |
| `[id, dispatch]` | Once on mount, then again whenever `id` or `dispatch` changes |

**In this app's three screens:**

```js
// HomeScreen — fetch products once on mount
useEffect(() => {
    dispatch(listProducts())
}, [dispatch])

// ProductScreen — re-fetch when the URL product id changes
useEffect(() => {
    dispatch(listProductDetails(id))
}, [id, dispatch])

// CartScreen — add item to cart when the page loads with an id in the URL
useEffect(() => {
    if (id) {
        dispatch(addToCart(id, qty))
    }
}, [dispatch, id, qty])
```

`dispatch` is listed in the dependency arrays because React's linting rules require it — in practice `dispatch` never actually changes, so those effects only run once.

---

### `useNavigate` — the v6 replacement for `history.push`

In React Router v5 the course uses `history.push('/path')` to redirect programmatically. In v6 this no longer works — use `useNavigate` instead:

```js
import { useNavigate } from 'react-router-dom'

const navigate = useNavigate()

navigate('/')     // redirect to home
navigate('/login') // redirect to login
navigate(-1)      // go back one page (replaces history.goBack())
```

In `LoginScreen`, you'll use this after a successful login to redirect the user to the home page (or wherever they came from).

---

### The complete login data flow — end to end

```
User fills in email + password → clicks "Login"
    ↓
LoginScreen: dispatch(login(email, password))
    ↓
thunk → dispatch USER_LOGIN_REQUEST
    → state.userLogin = { loading: true }
    → <Loader /> spinner shows
    ↓
axios.post('/api/users/login/', { username: email, password })
    ↓
Django: MyTokenObtainPairView → authenticate() → issue token
    ↓
Response: { _id, name, email, isAdmin, token }
    ↓
dispatch USER_LOGIN_SUCCESS, payload: data
    → state.userLogin = { loading: false, userInfo: { name, token, ... } }
    ↓
localStorage.setItem('userInfo', JSON.stringify(data))
    → survives page refresh
    ↓
navigate('/') → redirect to home
    → Header reads state.userLogin.userInfo → shows user name dropdown
```

---

### Key Concepts from this Section

**localStorage as persistent login**
Redux resets on page refresh. `localStorage` does not. By reading `userInfo` from `localStorage` at store init, the user stays logged in across refreshes without re-entering credentials. The token stored there is sent in the `Authorization` header on future protected requests.

**`useEffect` dependency array**
Controls *when* the effect re-runs. An empty array `[]` means once on mount. Adding values like `[id]` means "re-run if `id` changes." Always include every variable the effect uses — React's linter enforces this.

**`useNavigate` (v6) vs `history.push` (v5)**
React Router v6 removed route props like `history`. All navigation is done via the `useNavigate` hook: `const navigate = useNavigate()` → `navigate('/path')`.

**Error field key consistency**
The login reducer reads `action.error` (not `action.payload`). This matches what the product reducers do on failure. Pick one convention and stick to it across your codebase.

**Updated Redux state shape:**
```
store = {
    productList:    { loading, error, products }
    productDetails: { loading, error, product }
    cart:           { cartItems }
    userLogin:      { loading, error, userInfo }   ← NEW
}
```

---

### Register — constants, reducer, and action creator

**Three new constants added to `userConstants.js`:**

```js
export const USER_REGISTER_REQUEST = 'USER_REGISTER_REQUEST'
export const USER_REGISTER_SUCCESS = 'USER_REGISTER_SUCCESS'
export const USER_REGISTER_FAIL    = 'USER_REGISTER_FAIL'
```

---

**`userRegisterReducers` added to `userReducers.js`:**

```js
export const userRegisterReducers = (state = {}, action) => {
  switch (action.type) {
    case USER_REGISTER_REQUEST:
      return { loading: true }
    case USER_REGISTER_SUCCESS:
      return { loading: false, userInfo: action.payload }
    case USER_REGISTER_FAIL:
      return { loading: false, error: action.error }
    case USER_LOGOUT:
      return {}
    default:
      return state
  }
}
```

Structurally identical to `userLoginReducers`. It lives in `state.userRegister` (its own slice) and only responds to `USER_REGISTER_*` actions — plus `USER_LOGOUT` to wipe its state on logout.

---

**`register` action creator added to `userActions.js`:**

```js
export const register = (name, email, password) => async (dispatch) => {
  try {
    dispatch({ type: USER_REGISTER_REQUEST })

    const config = { headers: { 'Content-type': 'application/json' } }

    const { data } = await axios.post(
      '/api/users/register/',
      { email, password, name },
      config
    )

    dispatch({ type: USER_REGISTER_SUCCESS, payload: data })

    dispatch({ type: USER_LOGIN_SUCCESS, payload: data })   // ← key line

    localStorage.setItem('userInfo', JSON.stringify(data))

  } catch (error) {
    dispatch({
      type: USER_REGISTER_FAIL,
      error: error.response && error.response.data.detail
        ? error.response.data.detail
        : error.message,
    })
  }
}
```

**Why `USER_LOGIN_SUCCESS` is dispatched inside the register action:**

After a successful registration, the backend returns the same user data + token as a login response. Two things need to happen immediately:

1. The user should be **logged in** — meaning `state.userLogin.userInfo` must be set
2. The Header must **re-render** showing the user's name

`state.userLogin` is exclusively managed by `userLoginReducers`. The only way to update it is to dispatch an action it recognises — `USER_LOGIN_SUCCESS`. Redux broadcasts every dispatch to all reducers, so dispatching `USER_LOGIN_SUCCESS` here triggers `userLoginReducers` even though we're inside the register flow:

```
dispatch(USER_LOGIN_SUCCESS, payload: data)
    ↓
├── userRegisterReducers → no match → state unchanged
└── userLoginReducers    → case USER_LOGIN_SUCCESS matches!
                           → state.userLogin = { userInfo: data }
                           → Header re-renders with user's name
```

**`localStorage` vs live Redux — why both are needed:**

`localStorage.setItem` only helps on **page refresh** — the store reads it once at startup via `initialState`. During a live session, only a Redux dispatch updates the store.

| Scenario | What sets `state.userLogin.userInfo` |
|---|---|
| Page refresh after register/login | `localStorage` → `initialState` → store |
| Same session, no refresh | `dispatch(USER_LOGIN_SUCCESS)` → reducer → store |

Both paths must work, so both are needed.

---

### `logout` action creator

```js
export const logout = () => (dispatch) => {
  localStorage.removeItem('userInfo')
  dispatch({ type: USER_LOGOUT })
}
```

Not async — no API call needed. It does two things:
1. Removes `userInfo` from `localStorage` so the user doesn't reappear on next page load
2. Dispatches `USER_LOGOUT` — both `userLoginReducers` and `userRegisterReducers` handle this case, returning `{}` to wipe their state clean

---

### Header.jsx — conditional rendering based on login state

The Header now reads `state.userLogin` from the store and conditionally renders either a login link or a user dropdown:

```jsx
const userLogin = useSelector((state) => state.userLogin)
const { userInfo } = userLogin

const dispatch = useDispatch()

function logoutHandler() {
  dispatch(logout())
}

// In JSX:
{userInfo ? (
  <NavDropdown title={userInfo.name} id="username">
    <LinkContainer to="/profile">
      <NavDropdown.Item>Profile</NavDropdown.Item>
    </LinkContainer>
    <NavDropdown.Item onClick={logoutHandler}>
      Logout
    </NavDropdown.Item>
  </NavDropdown>
) : (
  <LinkContainer to="/login">
    <Nav.Link><i className="fas fa-user"></i>Login</Nav.Link>
  </LinkContainer>
)}
```

**How it works:**

- `userInfo` is `null` when nobody is logged in → renders the Login link
- `userInfo` is an object when logged in → renders a dropdown with the user's name as the title

The dropdown shows two options: **Profile** (navigates to `/profile`) and **Logout** (calls `logoutHandler` which dispatches `logout()`).

**`LinkContainer` from `react-router-bootstrap`:**
Wraps React Bootstrap nav components with React Router's `<Link>` behaviour. Without it, Bootstrap's `Nav.Link` uses a plain `<a href>` tag that causes a full page reload. `LinkContainer` makes it a client-side navigation without reload — same as `<Link>` but compatible with Bootstrap components.

**Why the Header reads `state.userLogin` and not `state.userRegister`:**
`state.userLogin.userInfo` is the single source of truth for whether a user is authenticated. Both the `login` and `register` actions populate it (register does so by also dispatching `USER_LOGIN_SUCCESS`). The Header only needs to watch one slice.

---

### The redirect pattern in RegisterScreen

`RegisterScreen` uses the same redirect pattern as `LoginScreen` — preserving the destination across the register/login flow:

```js
const [searchParams] = useSearchParams()
const redirect = searchParams.get('redirect') || '/'

useEffect(() => {
  if (userInfo) {
    navigate(redirect)
  }
}, [navigate, userInfo, redirect])
```

The "Already a customer?" link passes the redirect forward:
```jsx
<Link to={redirect ? `/login?redirect=${redirect}` : '/login'}>
  Login
</Link>
```

**Full redirect chain:**
```
User tries /shipping (checkout) → not logged in
    ↓
Redirected to /login?redirect=/shipping
    ↓
Clicks "Don't have an account? Register"
    ↓
Goes to /register?redirect=/shipping    ← redirect preserved
    ↓
Registers successfully → navigate('/shipping')  ← lands where they wanted
```

---

### Updated Redux state shape at end of Section 7

```
store = {
    productList:    { loading, error, products }
    productDetails: { loading, error, product }
    cart:           { cartItems }
    userLogin:      { loading, error, userInfo }   ← login + register both write here
    userRegister:   { loading, error, userInfo }   ← register only
}
```

`combineReducers` in `Store.jsx`:
```js
const reducer = combineReducers({
    productList:    productListReducers,
    productDetails: productDetailsReducers,
    cart:           cartReducer,
    userLogin:      userLoginReducers,
    userRegister:   userRegisterReducers    // ← NEW
})
```

Each key in `combineReducers` is the exact string you pass to `useSelector` — `state.userLogin`, `state.userRegister`, etc. The reducer only manages its own slice; other slices are untouched by its actions.

---

### User Profile — fetching and displaying profile data

This adds a profile page where a logged-in user can see their details and update them. It touches every layer: a new backend endpoint, new Redux constants/reducer/action, a new frontend page, and new routes.

---

#### Backend — two new views and a new URL

**`GetUserProfile`** — reads the logged-in user's data:

```python
class GetUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user                      # set automatically by JWTAuthentication
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
```

`request.user` is populated automatically by the `JWTAuthentication` middleware defined in `settings.py`. It reads the `Authorization: Bearer <token>` header on the request, decodes the JWT, looks up the matching user in the database, and attaches them to the request — all before your view code runs. You never have to write that lookup yourself.

**`UpdateUserProfile`** — updates the logged-in user's data:

```python
class UpdateUserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        user.first_name = data['name']
        user.username   = data['email']
        user.email      = data['email']

        if data['password'] != '':
            user.password = make_password(data['password'])

        user.save()

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
```

Key points:
- The serializer is created **after** `user.save()` — so it captures the updated state, not the old one
- `make_password()` hashes the new password before storing it — never store plain text passwords
- Password is only updated if the field is not empty — allows updating name/email without changing password
- Returns `UserSerializerWithToken` (not plain `UserSerializer`) so the frontend receives a fresh token to store in `localStorage`

**Why two separate views instead of one:**
`GET` uses `UserSerializer` (no token needed — just profile data). `PUT` uses `UserSerializerWithToken` (needs to return a token so the frontend can stay logged in after an update). Two different serializers = cleaner as two separate views.

**New URLs in `user_urls.py`:**

```python
path('profile/',        views.GetUserProfile.as_view(),    name='get_user_profile'),
path('profile/update/', views.UpdateUserProfile.as_view(), name='update_user_profile'),
```

Full assembled URLs:

```
GET  /api/users/profile/         → GetUserProfile   (read profile)
PUT  /api/users/profile/update/  → UpdateUserProfile (update profile)
```

---

#### How authentication works on these endpoints

Two separate mechanisms work together — they are NOT the same thing:

**Authentication** (`DEFAULT_AUTHENTICATION_CLASSES` in `settings.py`) — runs on **every** request, including public ones like login. It reads the token from the header, decodes it, and sets `request.user`. It never blocks a request — if no token is present it just sets `request.user = AnonymousUser` and moves on.

**Authorization** (`permission_classes` on the view) — runs after authentication and decides whether the identified user is allowed in:

```
Request hits /api/users/profile/
    ↓
JWTAuthentication runs (always)
    → token present + valid → request.user = User instance
    → token missing/invalid → request.user = AnonymousUser
    ↓
permission_classes = [IsAuthenticated] checks request.user
    → User instance    → allowed through → view runs
    → AnonymousUser    → 403 returned   → view never runs
```

The login endpoint has no `permission_classes` — it defaults to `AllowAny`, meaning anyone can hit it (which is correct — you need to be able to log in without a token).

---

#### Frontend — three new constants

```js
export const USER_DETAILS_REQUEST = 'USER_DETAILS_REQUEST'
export const USER_DETAILS_SUCCESS = 'USER_DETAILS_SUCCESS'
export const USER_DETAILS_FAIL    = 'USER_DETAILS_FAIL'
```

Same pattern as every other feature — shared string constants imported by both the action creator and the reducer.

---

#### Frontend — `userDetailsReducers`

```js
export const userDetailsReducers = (state = { user: {} }, action) => {
  switch (action.type) {
    case USER_DETAILS_REQUEST:
      return { ...state, loading: true }
    case USER_DETAILS_SUCCESS:
      return { loading: false, user: action.payload }
    case USER_DETAILS_FAIL:
      return { loading: false, error: action.error }
    default:
      return state
  }
}
```

Initial state is `{ user: {} }` — an empty object rather than `null`. This prevents the `ProfileScreen` from crashing when it tries to read `user.name` before the fetch completes, since accessing a property on `{}` returns `undefined` rather than throwing an error.

Notice `USER_DETAILS_REQUEST` uses `{ ...state, loading: true }` — it spreads the existing state and only adds `loading: true`. This keeps any previously fetched `user` data visible while a re-fetch is in progress, instead of blanking it out. Compare to `USER_DETAILS_SUCCESS` which returns a fresh object (old data is replaced by new data).

Registered in `Store.jsx`:
```js
const reducer = combineReducers({
    // ...existing slices
    userDetails: userDetailsReducers    // → state.userDetails
})
```

---

#### Frontend — `getUserDetails` action creator

```js
export const getUserDetails = (id) => async (dispatch, getState) => {
  try {
    dispatch({ type: USER_DETAILS_REQUEST })

    const { userLogin: { userInfo } } = getState()   // ← reads token from store

    const config = {
      headers: {
        'Content-type': 'application/json',
        'Authorization': `Bearer ${userInfo.token}`  // ← sends token to Django
      }
    }

    const { data } = await axios.get(`/api/users/${id}/`, config)

    dispatch({ type: USER_DETAILS_SUCCESS, payload: data })

  } catch (error) {
    dispatch({
      type: USER_DETAILS_FAIL,
      error: error.response && error.response.data.detail
        ? error.response.data.detail
        : error.message,
    })
  }
}
```

**`getState()` — reading from the store inside an action creator:**
`getState` is the second argument thunk injects (after `dispatch`). It returns the current Redux store state. Here it's used to pull the JWT token out of `state.userLogin.userInfo.token` — so the action can attach it to the request header.

The destructuring `const { userLogin: { userInfo } } = getState()` is shorthand for:
```js
const state = getState()
const userInfo = state.userLogin.userInfo
```

**Why `Authorization: Bearer ${userInfo.token}`:**
Django's `GetUserProfile` has `permission_classes = [IsAuthenticated]`. Without this header, `JWTAuthentication` finds no token, sets `request.user = AnonymousUser`, and the permission check returns 403. With the header, it decodes the token and grants access.

**Why `id` is passed as `"profile"`:**
```js
dispatch(getUserDetails("profile"))
```
The URL becomes `/api/users/profile/` — which matches the `GetUserProfile` endpoint. This is a deliberate reuse: the same action creator can later fetch any user by id (e.g. `getUserDetails(5)` → `/api/users/5/`) for admin functionality.

---

#### Frontend — `ProfileScreen.jsx`

```jsx
export default function ProfileScreen() {
  const [name, setName]                     = useState('')
  const [email, setEmail]                   = useState('')
  const [password, setPassword]             = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [message, setMessage]               = useState('')

  const userDetails = useSelector((state) => state.userDetails)
  const { loading, user, error } = userDetails

  const userLogin = useSelector((state) => state.userLogin)
  const { userInfo } = userLogin

  useEffect(() => {
    if (!userInfo) {
      navigate('/login')          // not logged in → redirect to login
    } else {
      if (!user || !user.name) {
        dispatch(getUserDetails('profile'))   // fetch profile from Django
      } else {
        setName(user.name)        // profile loaded → pre-fill the form fields
        setEmail(user.email)
      }
    }
  }, [dispatch, navigate, userInfo, user])
```

**Two `useSelector` calls — why both are needed:**

| Selector | Slice | Used for |
|---|---|---|
| `state.userLogin` | `userLoginReducers` | Check if logged in; get the token |
| `state.userDetails` | `userDetailsReducers` | The full profile data from the API |

`userInfo` (from `userLogin`) is the lightweight object stored after login — it has the token but may not have all profile fields. `user` (from `userDetails`) is the full profile fetched from `/api/users/profile/`.

**The `useEffect` logic step by step:**

```
Component mounts
    ↓
Is userInfo null?
    Yes → navigate('/login')   ← guard: redirect unauthenticated users
    No  ↓
Does user.name exist yet?
    No  → dispatch(getUserDetails('profile'))   ← fetch from Django
    Yes → setName(user.name), setEmail(user.email)  ← pre-fill form
```

The second condition `!user || !user.name` prevents re-fetching on every render. Once the profile is loaded into the store, the effect just pre-fills the form instead of making another API call.

**The form layout:**
```
Row
├── Col md=3   ← profile form (name, email, password, confirm password)
└── Col md=9   ← "My Orders" placeholder (orders feature added later)
```

**Password confirm check in `submitHandler`:**
```js
if (password !== confirmPassword) {
    setMessage('Passwords do not match!')
} else {
    // dispatch update action (added in next step)
}
```
`message` is local component state (not Redux) — it only lives in this component and doesn't need to be shared anywhere else. `setMessage` triggers a re-render that shows the `<Message>` component at the top of the form.

---

#### App.js — new route added

```js
<Route path='/profile' element={<ProfileScreen />} />
```

`ProfileScreen` handles its own auth guard internally (the `useEffect` redirect). No special protected route wrapper is needed — if `userInfo` is null, the effect fires immediately and navigates to `/login`.

---

#### Full data flow — loading the profile page

```
User navigates to /profile
    ↓
ProfileScreen mounts
    ↓
useEffect runs
    → userInfo exists? (from state.userLogin)
    → user.name exists? No → dispatch(getUserDetails('profile'))
    ↓
getUserDetails action:
    → dispatch USER_DETAILS_REQUEST → state.userDetails = { loading: true }
    → getState() grabs token from state.userLogin.userInfo.token
    → GET /api/users/profile/ with Authorization: Bearer <token>
    ↓
Django JWTAuthentication decodes token → request.user = User instance
permission_classes = [IsAuthenticated] → passes
GetUserProfile.get() → UserSerializer(user) → Response(data)
    ↓
    → dispatch USER_DETAILS_SUCCESS → state.userDetails = { user: { name, email, ... } }
    ↓
useEffect fires again (user changed in store)
    → user.name now exists → setName(user.name), setEmail(user.email)
    ↓
Form fields pre-filled with profile data
```

---

#### Updated Redux state shape at end of Section 7

```
store = {
    productList:    { loading, error, products }
    productDetails: { loading, error, product }
    cart:           { cartItems }
    userLogin:      { loading, error, userInfo }
    userRegister:   { loading, error, userInfo }
    userDetails:    { loading, error, user }        ← NEW
}
```

---

### Update User Profile — the final piece of Section 7

This adds the ability for a logged-in user to update their name, email, and password from the profile page.

---

#### New constants

Four new strings added to `userConstants.js`:

```js
export const USER_UPDATE_PROFILE_REQUEST = 'USER_UPDATE_PROFILE_REQUEST'
export const USER_UPDATE_PROFILE_SUCCESS = 'USER_UPDATE_PROFILE_SUCCESS'
export const USER_UPDATE_PROFILE_FAIL    = 'USER_UPDATE_PROFILE_FAIL'
export const USER_UPDATE_PROFILE_RESET   = 'USER_UPDATE_PROFILE_RESET'
```

Also one new constant for `userDetails`:
```js
export const USER_DETAILS_RESET = 'USER_DETAILS_RESET'
```

The `RESET` constants are new — explained below.

---

#### `userUpdateProfileReducers` — a new slice with a `success` flag

```js
export const userUpdateProfileReducers = (state = {}, action) => {
  switch (action.type) {
    case USER_UPDATE_PROFILE_REQUEST:
      return { ...state, loading: true }
    case USER_UPDATE_PROFILE_SUCCESS:
      return { loading: false, success: true, userInfo: action.payload }
    case USER_UPDATE_PROFILE_FAIL:
      return { loading: false, error: action.error }
    case USER_UPDATE_PROFILE_RESET:
      return {}
    default:
      return state
  }
}
```

**The `success: true` flag** is the key new idea. It's a boolean the component can watch with `useSelector`. When `success` becomes `true`, the `ProfileScreen` knows the update finished and can trigger a re-fetch of the profile. Without it, there'd be no way for the component to know the update completed.

**`USER_UPDATE_PROFILE_RESET`** wipes the slice back to `{}`. This is needed to clear `success` after it's been acted on — otherwise it stays `true` permanently and causes an infinite re-fetch loop.

Also added to `userDetailsReducers`:
```js
case USER_DETAILS_RESET:
  return { user: {} }
```

---

#### The RESET pattern — why it exists

RESET constants solve two stale-state problems:

**Problem 1 — After logout:**
`state.userDetails` still holds the previous user's profile after logout. If a different user logs in on the same session, they'd briefly see the old profile. The `logout` action now clears it:

```js
export const logout = () => (dispatch) => {
  localStorage.removeItem('userInfo')
  dispatch({ type: USER_LOGOUT })
  dispatch({ type: USER_DETAILS_RESET })   // ← wipes state.userDetails = { user: {} }
}
```

**Problem 2 — After a successful update:**
`success` stays `true` forever after an update. Since `success` is in the `useEffect` dependency array, it would trigger re-fetching on every render — an infinite loop. The fix is to reset it immediately after reacting to it:

```js
useEffect(() => {
  if (!user || !user.name || success) {
    dispatch({ type: USER_UPDATE_PROFILE_RESET })  // ← clears success immediately
    dispatch(getUserDetails('profile'))             // ← then re-fetches
  }
}, [user, success, ...])
```

The order matters: reset first, then fetch. If you fetched first, `success` would still be `true` when the effect ran again, causing another loop.

---

#### `updateUserProfile` action creator

```js
export const updateUserProfile = (user) => async (dispatch, getState) => {
  try {
    dispatch({ type: USER_UPDATE_PROFILE_REQUEST })

    const { userLogin: { userInfo } } = getState()   // ← get token from store

    const config = {
      headers: {
        'Content-type': 'application/json',
        'Authorization': `Bearer ${userInfo.token}`
      }
    }

    const { data } = await axios.put('/api/users/profile/update/', user, config)

    dispatch({ type: USER_UPDATE_PROFILE_SUCCESS, payload: data })

    dispatch({ type: USER_LOGIN_SUCCESS, payload: data })   // ← update Header too

    localStorage.setItem('userInfo', JSON.stringify(data))

  } catch (error) {
    dispatch({
      type: USER_UPDATE_PROFILE_FAIL,
      error: error.response && error.response.data.detail
        ? error.response.data.detail
        : error.message,
    })
  }
}
```

**`axios.put(url, data, config)`** — positional arguments, not named. Order is always: URL first, body data second, config (headers) third. JavaScript doesn't support named function arguments like Python does.

**Why `USER_LOGIN_SUCCESS` is dispatched again:**
Same reason as in `register` — `state.userLogin` is what the Header reads to show the user's name. If the user updates their name on the profile page, the Header dropdown must reflect the new name immediately. The only way to update `state.userLogin.userInfo` is to dispatch `USER_LOGIN_SUCCESS` with the new data. This is the same cross-slice trick used in the register flow.

**Why `localStorage` is updated:**
On page refresh, the store re-hydrates from `localStorage`. If the profile was updated but `localStorage` still has the old name/token, the store would start with stale data. Saving to `localStorage` here keeps it in sync.

---

#### `ProfileScreen` — the complete component

```js
const userDetails       = useSelector((state) => state.userDetails)
const { loading, user, error } = userDetails

const userLogin         = useSelector((state) => state.userLogin)
const { userInfo }      = userLogin

const userUpdateProfile = useSelector((state) => state.userUpdateProfile)
const { success }       = userUpdateProfile
```

Three `useSelector` calls — each reading a different slice for a different purpose:

| Slice | What it provides |
|---|---|
| `state.userLogin` | `userInfo` — checks if logged in, has the token |
| `state.userDetails` | `user` — full profile data from the API, pre-fills the form |
| `state.userUpdateProfile` | `success` — signals when an update has completed |

**The `useEffect` — full logic:**

```js
useEffect(() => {
  if (!userInfo) {
    navigate('/login')           // not logged in → redirect away
  } else {
    if (!user || !user.name || success) {
      dispatch({ type: USER_UPDATE_PROFILE_RESET })  // clear success flag
      dispatch(getUserDetails('profile'))             // fetch fresh profile
    } else {
      setName(user.name)         // profile loaded → pre-fill form
      setEmail(user.email)
    }
  }
}, [dispatch, navigate, userInfo, user, success])
```

The three conditions that trigger a fetch:
- `!user` — no profile data at all yet (first load)
- `!user.name` — profile object exists but is empty
- `success` — an update just completed, need fresh data

**The `submitHandler`:**

```js
function submitHandler(e) {
  e.preventDefault()

  if (password !== confirmPassword) {
    setMessage('Passwords do not match!')
  } else {
    dispatch(updateUserProfile({
      id:       user._id,
      name:     name,
      email:    email,
      password: password
    }))
    setMessage('')
  }
}
```

`e.preventDefault()` stops the browser's default form submit behaviour (which would reload the page). The password match check uses local component state (`message`) — this error only matters inside this component and doesn't need to be in Redux.

---

#### The complete update flow — end to end

```
User edits name/email/password → clicks Update
    ↓
submitHandler → passwords match? → dispatch(updateUserProfile({ id, name, email, password }))
    ↓
updateUserProfile action:
  → dispatch USER_UPDATE_PROFILE_REQUEST
    → state.userUpdateProfile = { loading: true }
    → getState() pulls token from state.userLogin.userInfo.token
    → PUT /api/users/profile/update/  with Authorization: Bearer <token>
    ↓
Django UpdateUserProfile view:
  → JWTAuthentication decodes token → request.user = User instance
  → IsAuthenticated passes
  → user.first_name = data['name'], user.email = data['email']
  → make_password(data['password']) if password not empty
  → user.save()
  → UserSerializerWithToken(user) → Response({ name, email, token, ... })
    ↓
  → dispatch USER_UPDATE_PROFILE_SUCCESS  → state.userUpdateProfile = { success: true, userInfo: data }
  → dispatch USER_LOGIN_SUCCESS           → state.userLogin = { userInfo: data }  ← Header updates
  → localStorage.setItem('userInfo', ...) ← persists across refresh
    ↓
useEffect fires (success changed to true)
  → dispatch USER_UPDATE_PROFILE_RESET    → state.userUpdateProfile = {}
  → dispatch getUserDetails('profile')    → re-fetches fresh profile from Django
    ↓
Profile re-fetched → USER_DETAILS_SUCCESS → state.userDetails = { user: { new data } }
    ↓
useEffect fires again (user changed)
  → user.name exists, success is false → setName/setEmail called
  → form pre-fills with updated data
```

---

#### Complete Redux state shape — end of Section 7

```
store = {
    productList:         { loading, error, products }
    productDetails:      { loading, error, product }
    cart:                { cartItems }
    userLogin:           { loading, error, userInfo }        ← login + register + update all write here
    userRegister:        { loading, error, userInfo }
    userDetails:         { loading, error, user }            ← full profile, reset on logout
    userUpdateProfile:   { loading, error, success, userInfo } ← NEW, reset after success
}
```

**The cross-slice dispatch pattern used in this app:**

Three different action creators dispatch `USER_LOGIN_SUCCESS` to update `state.userLogin`:

| Action creator | Why it also dispatches USER_LOGIN_SUCCESS |
|---|---|
| `login` | It IS the login — primary use |
| `register` | Auto-logs in after registration |
| `updateUserProfile` | Updates Header name after profile change |

This works because Redux broadcasts every action to all reducers. `userLoginReducers` reacts to `USER_LOGIN_SUCCESS` regardless of which action creator fired it.

---

---

## Section 8 — Checkout Flow (Cart → Login → Shipping)

### What was built

The checkout flow: a user clicks "Proceed to Checkout" in the cart, gets redirected to login if not authenticated (with a redirect back after), and lands on a shipping form that saves the address to Redux and localStorage.

**Files created:**
- `frontend/src/pages/ShippingScreen.jsx` — shipping address form

**Files modified:**
- `frontend/src/pages/CartScreen.jsx` — `checkoutHandler` now checks auth before redirecting
- `frontend/src/pages/LoginScreen.jsx` — fixed wrong query param name (`search` → `redirect`)
- `frontend/src/App.js` — added `/shipping` route
- `frontend/src/actions/cartActions.js` — added `saveShippingAddresss` action
- `frontend/src/reducers/cartReducers.js` — added `CART_SAVE_SHIPPING_ADDRESS` case

---

### The checkout flow end-to-end

```
User clicks "Proceed to Checkout"
        ↓
checkoutHandler() in CartScreen
        ↓
Is userInfo in Redux? ──Yes──► navigate('/shipping')
        │
       No
        ↓
navigate('/login?redirect=shipping')
        ↓
LoginScreen reads ?redirect=shipping
        ↓
User logs in → useEffect sees userInfo → navigate('/shipping')
        ↓
ShippingScreen — form fills from cart.shippingAddress (pre-filled if returning)
        ↓
Submit → saveShippingAddresss() dispatched → navigate('/payment')
```

---

### CartScreen.jsx — checkoutHandler

```jsx
const userLogin = useSelector((state) => state.userLogin);
const { userInfo } = userLogin;

function checkoutHandler() {
  if (userInfo) {
    navigate('/shipping')         // already logged in → go straight there
  } else {
    navigate('/login?redirect=shipping')  // not logged in → login first
  }
}
```

**Why read `userInfo` from Redux and not from localStorage directly:**
Redux is the single source of truth for auth state at runtime. `userInfo` is populated from localStorage when the store is initialized (in `store.js`), so it's always in sync.

---

### LoginScreen.jsx — redirect after login

```jsx
const redirect = searchParams.get("redirect") || "/";

useEffect(() => {
  if (userInfo) {
    navigate(redirect);   // goes to 'shipping' if ?redirect=shipping was in the URL
  }
}, [navigate, userInfo, redirect]);
```

**Bug that was fixed:** the original code had `searchParams.get("search")` instead of `searchParams.get("redirect")`. The param name must match exactly what the sender puts in the URL — `?redirect=shipping` requires `.get("redirect")`.

---

### saveShippingAddresss action + reducer

**Action** (`cartActions.js`):
```js
export const saveShippingAddresss = (data) => (dispatch) => {
  dispatch({ type: CART_SAVE_SHIPPING_ADDRESS, payload: data })
  localStorage.setItem('shippingAddress', JSON.stringify(data))
}
```

**Reducer** (`cartReducers.js`):
```js
case CART_SAVE_SHIPPING_ADDRESS:
  return {
    ...state,
    shippingAddress: action.payload
  }
```

Same pattern as `addToCart`: dispatch → reducer updates state → persist to localStorage so the address survives a page refresh.

---

### ShippingScreen.jsx — the form

```jsx
const cart = useSelector((state) => state.cart)
const { shippingAddress } = cart

const [address, setAddress]       = useState(shippingAddress.address)
const [city, setCity]             = useState(shippingAddress.city)
const [postalCode, setPostalCode] = useState(shippingAddress.postalCode)
const [country, setCountry]       = useState(shippingAddress.country)

function submitHandler(e) {
  e.preventDefault()
  dispatch(saveShippingAddresss({ address, city, postalCode, country }))
  navigate('/payment')
}
```

**Why initialize state from `shippingAddress`:**
If the user already went through shipping before (e.g. came back to edit the cart), the address is already in Redux/localStorage. Pre-filling the form from that state means they don't have to retype it.

**`value={address ? address : ""}`:**
On first visit `shippingAddress` is an empty object `{}`, so `address` is `undefined`. React controlled inputs require a defined value — `undefined` makes React treat it as uncontrolled. The fallback `""` keeps it controlled from the start.

---

### React Router v5 → v6: `useHistory` → `useNavigate`

| v5 | v6 |
|---|---|
| `const history = useHistory()` | `const navigate = useNavigate()` |
| `history.push('/path')` | `navigate('/path')` |
| `history.goBack()` | `navigate(-1)` |

`useHistory` no longer exists in v6 — always use `useNavigate`.

---

### Updated Redux state shape — end of Section 8

```
store = {
    productList:         { loading, error, products }
    productDetails:      { loading, error, product }
    cart:                { cartItems, shippingAddress }   ← shippingAddress added
    userLogin:           { loading, error, userInfo }
    userRegister:        { loading, error, userInfo }
    userDetails:         { loading, error, user }
    userUpdateProfile:   { loading, error, success, userInfo }
}
```

---

---

### Section 8 continued — Payment Method, Checkout Steps, Place Order & Create Order (videos 48–52)

This continues from where the existing Section 8 left off (shipping screen). The notes below cover the payment method screen, checkout steps component, place order screen, and the full order backend + Redux layer.

**New files:**
- `frontend/src/pages/PlaceOrderScreen.jsx` — order summary + "Place Order" button
- `frontend/src/constants/orderConstants.js` — `ORDER_CREATE_*` constants
- `frontend/src/reducers/orderReducers.js` — `orderCreateReducer`
- `frontend/src/actions/orderActions.js` — `createOrder` async action creator

**Files updated:**
- `backend/api/serializers.py` — added `OrderSerializer`, `OrderItemSerializer`, `ShippingAddressSerializer`
- `backend/api/urls/order_urls.py` — wired `POST /api/orders/add/`
- `backend/api/views/order_views.py` — `OrderItemsAPI` creates the full order
- `frontend/src/Store.jsx` — registered `orderCreateReducer`

---

#### Payment Method — Redux slice (video 49)

Follows the same constants → reducer → action → localStorage pattern as `saveShippingAddresss` (see existing Section 8). Schema only:

```
CART_SAVE_PAYMENT_METHOD constant
cartReducer: CART_SAVE_PAYMENT_METHOD case → { ...state, paymentMethod: action.payload }
savePaymentMethod action → dispatch → localStorage.setItem('paymentMethod', ...)
Store.jsx: paymentMethodFromStorage hydrates cart.paymentMethod on init
```

`PaymentScreen.jsx` reads `cart.shippingAddress` as a guard (if no address → redirect to `/shipping`), collects the payment choice via a radio button, then dispatches `savePaymentMethod` and navigates to `/placeorder`.

---

#### Checkout Steps Component (video 48)

`CheckOutSteps.jsx` is a purely presentational component that receives boolean props (`step1`, `step2`, `step3`, `step4`) and renders a progress bar showing which checkout step the user is on. No Redux — no state, no dispatch. Just props controlling which steps are highlighted.

```jsx
<CheckOutSteps step1 step2 step3 step4 />   // all four active on PlaceOrderScreen
<CheckOutSteps step1 step2 step3 />          // three active on PaymentScreen
```

Every checkout screen renders `<CheckOutSteps>` at the top with the appropriate props.

---

#### Backend — Nested OrderSerializer (video 51)

The `OrderSerializer` needs to embed related objects (items, shipping address, user) that live in separate tables. This uses `SerializerMethodField` — the same pattern documented in [Section 6 — UserSerializer](#serializerspy----userserializer-and-userserializerwithtoken). Schema and new concept only:

```python
class OrderSerializer(serializers.ModelSerializer):
    orderItems      = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user            = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()         # ← reverse FK lookup (new concept below)
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(obj.shippingAddress, many=False)
        except Exception:
            address = False
        return address

    def get_user(self, obj):
        serializer = UserSerializer(obj.user, many=False)
        return serializer.data
```

**New concept — `obj.orderitem_set.all()` (reverse FK lookup):**

Because `OrderItem` has `order = ForeignKey(Order, ...)`, Django automatically creates a reverse manager on `Order`. You can access all items belonging to an order without writing a query:

```
order.orderitem_set.all()   →  SELECT * FROM orderitem WHERE order_id = <this order's id>
```

The naming convention: `<lowercase_model_name>_set`. So `OrderItem` → `orderitem_set`, `Review` → `review_set`, etc.

**Nested serializers** — `get_orderItems` uses `OrderItemSerializer` *inside* `OrderSerializer`. This embeds the full list of items in the order JSON response, so the frontend doesn't need a second request to get them.

**URL:**
```
backend/urls.py:    path('api/orders/', include('api.urls.order_urls'))
order_urls.py:      path('add/', views.OrderItemsAPI.as_view(), name='orders-add')
→ Full URL: POST /api/orders/add/
```

---

#### Backend — OrderItemsAPI view (video 51–52)

```python
class OrderItemsAPI(APIView):
    permission_classes = [IsAuthenticated]   # same pattern as Section 6

    def post(self, request):
        user = request.user      # set by JWTAuthentication from the token header
        data = request.data

        order_items = data['orderItems']
        if order_items and len(order_items) == 0:
            return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)

        # Create in dependency order: Order first, then its children
        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )
        ShippingAddress.objects.create(
            order=order, address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )
        for i in order_items:
            product = Product.objects.get(_id=i['product'])
            item = OrderItem.objects.create(
                order=order, product=product, name=product.name,
                quantity=i['qty'],           # ← model field is `quantity`, not `qty`
                price=i['price'],
                image=product.image.url,     # .url gives the servable URL, not just the path
            )
            product.countInStock -= item.quantity
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
```

**Key points:**
- Records must be created in FK dependency order: `Order` first → `ShippingAddress` (needs `order` FK) → `OrderItems` (each needs `order` and `product` FKs).
- **`product.image.url`** — `ImageField` stores a relative path on disk. `.url` returns the full URL Django will serve it at. Storing the URL on `OrderItem` at order-time preserves the image in order history even if the product image changes later.
- **`quantity` vs `qty`** — the frontend sends `qty` (how items are named in the cart), but the Django `OrderItem` model field is named `quantity`. Always use the exact model field name when calling `objects.create()`. This is a common source of `TypeError: got unexpected keyword arguments`.
- Decrements `countInStock` after each item — keeps inventory accurate.

---

#### Frontend — Order Redux (video 52)

Follows the identical constants → reducer → action creator → Store registration pattern documented in [Section 4 (product Redux)](#the-four-files-and-what-each-one-does) and [Section 7 (user Redux)](#userreducersjs----the-login-state-machine). Schema only:

**`orderConstants.js`:**
```
ORDER_CREATE_REQUEST | ORDER_CREATE_SUCCESS | ORDER_CREATE_FAIL
```

**`orderCreateReducer` state shape:**

| Action | State |
|---|---|
| `ORDER_CREATE_REQUEST` | `{ loading: true }` |
| `ORDER_CREATE_SUCCESS` | `{ loading: false, success: true, order: data }` |
| `ORDER_CREATE_FAIL` | `{ loading: false, error: ... }` |
| default | `{ ...state }` |

**`createOrder` action creator** — same JWT header pattern as `getUserDetails` (Section 7):

```js
export const createOrder = (order) => async (dispatch, getState) => {
  dispatch({ type: ORDER_CREATE_REQUEST })

  const { userLogin: { userInfo } } = getState()   // pull token from store

  const config = {
    headers: {
      'Content-type': 'application/json',
      Authorization: `Bearer ${userInfo.token}`,   // protected endpoint requires token
    }
  }

  const { data } = await axios.post(`/api/orders/add/`, order, config)
  dispatch({ type: ORDER_CREATE_SUCCESS, payload: data })
  // ... catch → ORDER_CREATE_FAIL
}
```

For the full explanation of `getState()` and the JWT header pattern, see [Section 7 — getUserDetails action creator](#frontend----getuserdetails-action-creator).

**`Store.jsx`:**
```js
orderCreate: orderCreateReducer   // → state.orderCreate
```

---

#### Frontend — PlaceOrderScreen.jsx (video 50)

The final checkout step — shows the full order summary and triggers order creation.

**Price calculations (computed in the component, not stored in Redux):**
```js
cart.itemPrice     = cart.cartItems.reduce((acc, item) => acc + item.price * item.qty, 0).toFixed(2)
cart.shippingPrice = (cart.itemPrice > 100 ? 0 : 10).toFixed(2)   // free over $100
cart.taxPrice      = Number(cart.itemPrice * 0.12).toFixed(2)
cart.totalPrice    = (Number(cart.itemPrice) + Number(cart.shippingPrice) + Number(cart.taxPrice)).toFixed(2)
```

These are derived from `cartItems` — no reason to store in Redux since they can always be recalculated.

**Two `useEffect` guards:**
```js
// Guard 1 — no payment method → redirect back to payment page
useEffect(() => {
  if (!cart.paymentMethod) navigate('/payment')
}, [cart.paymentMethod, navigate])

// Guard 2 — order successfully created → navigate to order detail
useEffect(() => {
  if (success) navigate(`/order/${order._id}`)
}, [success, navigate, order])
```

Both guards must be in `useEffect` — see [the rule explained in Section 7](#useeffect----the-hook-that-triggers-async-work-after-render). Calling `navigate()` directly in the render body is a side effect that causes React to behave unpredictably (the navigation may silently not fire).

**`placeOrder` handler:**
```js
function placeOrder() {
  dispatch(createOrder({
    orderItems: cart.cartItems, shippingAddress: cart.shippingAddress,
    paymentMethod: cart.paymentMethod, itemsPrice: cart.itemsPrice,
    shippingPrice: cart.shippingPrice, taxPrice: cart.taxPrice,
    totalPrice: cart.totalPrice,
  }))
}
```

All data comes from the Redux `cart` slice — no local state. The component reads the store and sends it straight to the backend.

---

#### Complete Place Order data flow

```
User on /placeorder → clicks "Place Order"
    ↓
dispatch(createOrder({ ...cartData }))
    ↓
ORDER_CREATE_REQUEST → state.orderCreate = { loading: true }
    ↓
POST /api/orders/add/  Authorization: Bearer <token>
  Body: { orderItems, shippingAddress, paymentMethod, taxPrice, shippingPrice, totalPrice }
    ↓
Django OrderItemsAPI:
  JWTAuthentication decodes token → request.user = User
  IsAuthenticated passes
  Order.objects.create(...)
  ShippingAddress.objects.create(order=order, ...)
  For each item:
    OrderItem.objects.create(order, product, quantity=i['qty'], ...)
    product.countInStock -= item.quantity; product.save()
  OrderSerializer(order) → nested JSON { order + items[] + shippingAddress + user }
    ↓
ORDER_CREATE_SUCCESS → state.orderCreate = { loading: false, success: true, order: data }
    ↓
useEffect sees success → navigate(`/order/${order._id}`)
```

---

#### Updated Redux state shape

```
store = {
    productList:         { loading, error, products }
    productDetails:      { loading, error, product }
    cart:                { cartItems, shippingAddress, paymentMethod }
    userLogin:           { loading, error, userInfo }
    userRegister:        { loading, error, userInfo }
    userDetails:         { loading, error, user }
    userUpdateProfile:   { loading, error, success, userInfo }
    orderCreate:         { loading, error, success, order }   ← NEW
}
```

**localStorage persistence — full picture:**

| Key | Saved when | Restored at store init |
|---|---|---|
| `cartItems` | Every cart add / remove | `cart.cartItems` |
| `shippingAddress` | Shipping form submit | `cart.shippingAddress` |
| `paymentMethod` | Payment form submit | `cart.paymentMethod` |
| `userInfo` | Login / register / profile update | `userLogin.userInfo` |

Orders are **not** persisted to localStorage — they live in the Django database and are fetched on demand.

---

#### Clearing the cart after placing an order

Once the order is successfully created on the backend, the cart should be emptied. This requires one new constant and a new reducer case.

**New constant in `cartConstants.js`:**
```js
export const CART_CLEAR_ITEMS = 'CART_CLEAR_ITEMS'
```

**New case in `cartReducers.js`:**
```js
case CART_CLEAR_ITEMS:
  return {
    ...state,
    cartItems: []
  }
```

**Dispatched inside `createOrder` after success:**
```js
dispatch({ type: ORDER_CREATE_SUCCESS, payload: data })

dispatch({ type: CART_CLEAR_ITEMS })          // wipe cart in Redux store

localStorage.removeItem('cartItems')          // wipe cart from localStorage
```

**Why both Redux and localStorage must be cleared:**
Redux holds the live in-memory cart for the current session. localStorage holds the persisted copy that survives page refresh. If you only cleared Redux, the cart would reappear on the next page load. If you only cleared localStorage, the cart would still show in the current session until refresh. Both must be removed.

**Order of operations matters:**
```
createOrder POSTs to backend
    ↓
Django creates Order, OrderItem, ShippingAddress records → decrements countInStock
    ↓
ORDER_CREATE_SUCCESS dispatched (order saved in state.orderCreate)
    ↓
CART_CLEAR_ITEMS dispatched (cartItems = [] in state.cart)
    ↓
localStorage.removeItem('cartItems') (cart gone on next refresh too)
    ↓
useEffect sees success → navigate(`/orders/${order._id}`)
```

The cart is cleared **after** the backend confirms the order — never before. If the API call failed you'd want the cart intact so the user can retry.

---

---

## Section 9 — Get Order by ID API

### What was built

A backend endpoint to retrieve a single order by its ID, accessible only to the order owner or an admin. No frontend screen was built yet — this section focuses on the Django backend and the URL configuration.

**Files modified:**
- `backend/api/views/order_views.py` — added `OrderIdAPI` class
- `backend/api/urls/order_urls.py` — added `<str:pk>/` route

---

### Backend — OrderIdAPI view

```python
class OrderIdAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            order = Order.objects.get(_id=pk)
            user = request.user

            if user.is_staff or order.user == user:
                serializer = OrderSerializer(order, many=False)
                return Response(serializer.data)
            else:
                return Response(
                    {'detail': 'Not Authorized to view this order'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {'detail': 'Order does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
```

**Two-layer access check:**

`permission_classes = [IsAuthenticated]` is the outer gate — rejects anyone without a valid token before the view body runs. But being authenticated is not enough on its own: you shouldn't be able to view someone else's order just because you're logged in. The inner `if` check handles that:

```
request.user.is_staff   → admin can see any order
order.user == user      → the order belongs to the logged-in user
```

If neither is true, a `400` response is returned. Note: this should arguably be a `403 Forbidden` instead of `400 Bad Request`, but `400` is what the course uses.

**Why `try/except` instead of `get_object_or_404`:**
If `Order.objects.get(_id=pk)` finds no matching record, it raises a `DoesNotExist` exception. The `except` block catches that (and any other exception) and returns a friendly JSON error instead of a raw Django 500 error page.

**The `OrderSerializer` response includes nested data:**
Because `OrderSerializer` uses `SerializerMethodField` for `orderItems`, `shippingAddress`, and `user` (see the serializer section in Section 8), the single response embeds everything the frontend order detail page will need — no second requests required.

---

### URL

```python
# order_urls.py
urlpatterns = [
    path('add/', views.OrderItemsAPI.as_view(), name='orders-add'),
    path('<str:pk>/', views.OrderIdAPI.as_view(), name='user-order'),
]
```

Assembled with the project-level prefix:
```
GET /api/orders/<pk>/   →   OrderIdAPI   (authenticated owner or admin only)
```

`<str:pk>` captures the order `_id` from the URL and passes it into the view as the `pk` keyword argument. The `_id` field is Django's `AutoField` primary key — it's an integer, but `<str:pk>` captures it as a string anyway. Django's ORM handles the type coercion when it runs `Order.objects.get(_id=pk)`.

**Complete URL table for the orders feature:**

| Endpoint | Method | Auth | Who | What |
|---|---|---|---|---|
| `/api/orders/add/` | POST | Authenticated | Any logged-in user | Create an order |
| `/api/orders/<pk>/` | GET | Authenticated | Owner or admin | Fetch one order by ID |

---

### Q&A from this session

**Q: How do you configure query params in Django URLs?**

You don't — query params (`?page=2`, `?status=paid`) are never defined in `urls.py`. Django makes them available in every view automatically via `request.GET`:

```python
def get_orders(request):
    status = request.GET.get('status')   # reads ?status=paid from the URL
```

`urls.py` only defines the URL path structure (e.g. `/orders/<pk>/`). Query strings are free-form and parsed at the view level.

**Q: How do you access the DRF browsable API login page?**

The project already has a JWT token endpoint at `POST /api/users/login/`. For protected endpoints, you pass the token in the `Authorization: Bearer <token>` header. There is no browser login form for the browsable API — use a tool like Postman or Thunder Client (VS Code extension) to test protected endpoints.

---

## Section 11 — Admin Screen Part 2 (Products & Orders CRUD)

**Lessons:** 65–73  
**Commits:** `f843b40` (product admin), `b1a8c26` (order admin)

### What was built

Full admin management for **products** (list, create, edit, delete, image upload) and **orders** (list all, view detail, mark as delivered). This is the second admin section — Section 10 covered user management.

**Files created:**
- `frontend/src/pages/ProductListScreen.jsx` — admin product list with create + delete buttons
- `frontend/src/pages/ProductEditScreen.jsx` — form to edit all product fields + image upload
- `frontend/src/pages/OrderListScreen.jsx` — admin view of every order placed on the site

**Files modified:**
- `backend/api/views/product_views.py` — added `DeleteProduct`, `CreateProduct`, `UpdateProduct`, `UploadImage` views
- `backend/api/urls/product_urls.py` — registered the four new product endpoints
- `backend/api/views/order_views.py` — added `AllOrders` (list every order) and `OrderDelivered` (mark delivered)
- `backend/api/urls/order_urls.py` — registered the two new order endpoints
- `backend/api/models.py` + migration `0005` — minor product image field change
- `frontend/src/actions/productActions.js` — added `deleteProduct`, `createProduct`, `updateProduct` Redux actions
- `frontend/src/reducers/productReducers.js` — added reducers for delete, create, update
- `frontend/src/constants/productConstants.js` — added constants for the three new action types
- `frontend/src/actions/orderActions.js` — added `listOrders`, `deliverOrder` actions
- `frontend/src/reducers/orderReducers.js` — added `orderListReducer`, `orderDeliverReducer`
- `frontend/src/constants/orderConstants.js` — added `ORDER_LIST_*` and `ORDER_DELIVERED_*` constants
- `frontend/src/pages/OrderScreen.jsx` — added "Mark as Delivered" button (admin only) + deliver Redux wiring
- `frontend/src/App.js` — added routes for `/admin/productlist/`, `/admin/product/:id/edit/`, `/admin/orderlist/`
- `frontend/public/images/placeholder.png` — default image used when a new product is created

---

### Backend — New Product Endpoints

```python
# backend/api/views/product_views.py

class DeleteProduct(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        product = Product.objects.get(_id=pk)
        product.delete()
        return Response('Product Deleted')

class CreateProduct(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user = request.user
        product = Product.objects.create(
            user=user,
            name='Sample Name',
            price=0,
            brand='Sample Brand',
            countInStock=0,
            category='Sample Category',
            description=''
        )
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

class UpdateProduct(APIView):
    def put(self, request, pk):
        data = request.data
        product = Product.objects.get(_id=pk)
        product.name = data['name']
        product.price = data['price']
        # ... (all fields updated then saved)
        product.save()
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

class UploadImage(APIView):
    def post(self, request):
        product_id = request.data['product_id']
        product = Product.objects.get(_id=product_id)
        product.image = request.FILES.get('image')   # multipart/form-data
        product.save()
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
```

**Key concept — `request.FILES`:** When an HTML form uploads a file, Django puts the binary file data in `request.FILES`, not `request.data`. You must send the request with `Content-Type: multipart/form-data` (not JSON). React does this automatically when you use `FormData`.

```python
# backend/api/urls/product_urls.py
urlpatterns = [
    path('',                    views.GetProducts.as_view(),   name='get_products'),
    path('create/',             views.CreateProduct.as_view(), name='create_product'),
    path('upload/',             views.UploadImage.as_view(),   name='image_upload'),
    path('<str:pk>',            views.GetProduct.as_view(),    name='user_order'),
    path('update/<str:pk>/',    views.UpdateProduct.as_view(), name='update_product'),
    path('delete/<str:pk>/',    views.DeleteProduct.as_view(), name='delete_product'),
]
```

**Complete product URL table:**

| Endpoint | Method | Auth | What |
|---|---|---|---|
| `GET /api/products/` | GET | Public | List all products |
| `POST /api/products/create/` | POST | Admin | Create placeholder product |
| `PUT /api/products/update/<pk>/` | PUT | Admin | Update product fields |
| `DELETE /api/products/delete/<pk>/` | DELETE | Admin | Delete a product |
| `GET /api/products/<pk>` | GET | Public | Get single product |
| `POST /api/products/upload/` | POST | Any | Upload product image |

---

### Backend — New Order Endpoints

```python
# backend/api/views/order_views.py

class AllOrders(APIView):
    permission_classes = [IsAdminUser]

    def get(self, _request):
        orders = Order.objects.all()   # no filter — admin sees everything
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDelivered(APIView):
    permission_classes = [IsAdminUser]

    def put(self, _request, pk):
        order = Order.objects.get(_id=pk)
        order.isDelivered = True
        order.deliveredAt = datetime.now()
        order.save()
        return Response('Order was delivered.')
```

```python
# backend/api/urls/order_urls.py
urlpatterns = [
    path('',                        views.AllOrders.as_view(),      name='orders'),
    path('add/',                    views.OrderItemsAPI.as_view(),  name='orders-add'),
    path('myorders/',               views.userOrders.as_view(),     name='my-orders'),
    path('<str:pk>/deliver/',       views.OrderDelivered.as_view(), name='order-delivered'),
    path('<str:pk>/',               views.OrderIdAPI.as_view(),     name='user-order'),
]
```

**Key concept — URL ordering matters:** `<str:pk>/deliver/` must come before `<str:pk>/` in `urlpatterns`. Django matches URLs top-to-bottom. If the `<str:pk>/` pattern came first, a request to `/api/orders/5/deliver/` would match it (with `pk="5/deliver"`) before ever reaching the deliver route.

---

### Frontend — ProductListScreen

The admin product list page (`/admin/productlist/`):

```jsx
// Pattern: dispatch delete → useEffect watches successDelete → re-fetches list
function deleteHandler(productId) {
  if (window.confirm("Are you sure you want to delete this product?")) {
    dispatch(deleteProduct(productId));
  }
}

function createProductHandler() {
  dispatch(createProduct());  // creates placeholder on backend
}

// In useEffect:
if (successCreated) {
  navigate(`/admin/product/${createdProduct._id}/edit`);  // go straight to edit
}
```

**Create-then-redirect pattern:** Instead of opening a blank form, the app calls the API to create a placeholder product (with default values like "Sample Name"), then immediately redirects to the edit screen for that new product. This means there's always a real DB record to save against — no orphaned form state.

**Why `PRODUCT_CREATE_RESET` at the top of useEffect?** Without this reset, `successCreated` stays `true` in Redux state after you land on the edit page, which would cause an infinite redirect loop when you come back to the list. Resetting it clears the flag.

---

### Frontend — ProductEditScreen

The edit form (`/admin/product/:id/edit/`):

```jsx
// Load product into local state when the component mounts
useEffect(() => {
  if (successUpdate) {
    dispatch({ type: PRODUCT_UPDATE_RESET });
    navigate('/admin/productlist/');
  } else {
    if (!product.name || product._id !== Number(productId)) {
      dispatch(listProductDetails(productId));   // fetch from API
    } else {
      setName(product.name);    // populate form fields from Redux state
      setPrice(product.price);
      // ... etc
    }
  }
}, [product, dispatch, productId, navigate, successUpdate]);
```

**Image upload — two inputs, one field:**
```jsx
<Form.Control type="text" value={image} onChange={(e) => setImage(e.target.value)} />
<Form.Control type="file" onChange={uploadFileHandler} />
```
The text input lets you paste a URL manually. The file input triggers `uploadFileHandler` which sends the binary file to `/api/products/upload/` via `multipart/form-data`. When the upload succeeds, `setImage(data.image)` updates the local state with the server path — the same `image` field the form will submit on save.

```jsx
async function uploadFileHandler(e) {
  const file = e.target.files[0];
  const formData = new FormData();
  formData.append('image', file);
  formData.append('product_id', productId);

  const config = { headers: { 'Content-Type': 'multipart/form-data' } };
  const { data } = await axios.post('/api/products/upload/', formData, config);
  setImage(data.image);
}
```

**Key concept — `FormData`:** This is the browser's built-in object for sending files over HTTP. When you `append` a `File` to it and POST it, the browser automatically encodes it as `multipart/form-data`. You cannot send binary files as JSON.

---

### Frontend — OrderListScreen

The admin order list (`/admin/orderlist/`). Only accessible to admins:

```jsx
useEffect(() => {
  if (userInfo && userInfo.isAdmin) {
    dispatch(listOrders());   // fetches GET /api/orders/ — all orders
  } else {
    navigate('/login');
  }
}, [dispatch, navigate, userInfo]);
```

The table shows: ID, username, date, total, paid date (or red X), delivered date (or red X), and a "Details" link that goes to `/order/:id` — the same order detail screen regular users see, but with the "Mark as Delivered" button shown for admins.

---

### Frontend — Mark as Delivered (OrderScreen)

The `OrderScreen.jsx` was updated to add admin-only deliver functionality:

```jsx
// New Redux state slice
const orderDeliver = useSelector((state) => state.orderDeliver);
const { loading: loadingDeliver, success: successDeliver } = orderDeliver;

// useEffect now also resets deliver state and re-fetches when successDeliver fires
if (!order || successPay || order._id !== Number(id) || successDeliver) {
  dispatch({ type: ORDER_PAY_RESET });
  dispatch({ type: ORDER_DELIVERED_RESET });
  dispatch(getOrderDetails(id));
}

function deliverHandler() {
  dispatch(deliverOrder(order));
}
```

The "Mark as Delivered" button only renders when `userInfo.isAdmin` is true, so regular users never see it.

---

### Redux — New Actions (Products)

Three new thunk actions added to `productActions.js`:

| Action | API call | When used |
|---|---|---|
| `deleteProduct(id)` | `DELETE /api/products/delete/:id/` | Admin clicks trash icon |
| `createProduct()` | `POST /api/products/create/` | Admin clicks "Create Product" |
| `updateProduct(product)` | `PUT /api/products/update/:id/` | Admin submits edit form |

All three follow the same three-step pattern: dispatch `_REQUEST` → call API with auth header → dispatch `_SUCCESS` or `_FAIL`.

### Redux — New Actions (Orders)

| Action | API call | When used |
|---|---|---|
| `listOrders()` | `GET /api/orders/` | Admin loads order list page |
| `deliverOrder(order)` | `PUT /api/orders/:id/deliver/` | Admin clicks "Mark as Delivered" |

---

### Key Concepts Summary

| Concept | What to remember |
|---|---|
| `IsAdminUser` permission | DRF built-in — blocks anyone where `is_staff=False`. All admin endpoints use this. |
| Create-then-redirect | Create a DB record first with defaults, then redirect to its edit form. Avoids orphaned form state. |
| `PRODUCT_CREATE_RESET` | Must reset success flags in `useEffect` or the redirect triggers in a loop. |
| `request.FILES` | Binary file uploads land here, not in `request.data`. Requires `multipart/form-data`. |
| `FormData` | Browser API to send files over HTTP. Pass it to `axios.post` with `Content-Type: multipart/form-data`. |
| URL ordering | More specific paths (`<pk>/deliver/`) must be listed before catch-all paths (`<pk>/`) in Django `urlpatterns`. |
| Two image inputs | Text field for URL path + file input for upload — both control the same `image` state variable. |

---

*More sections will be added as the course progresses.*
