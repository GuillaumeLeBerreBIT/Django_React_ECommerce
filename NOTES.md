# ProShop — Django + React E-Commerce (Udemy Course Notes)

> **Course:** [Django with React | An Ecommerce Website](https://www.udemy.com/course/django-with-react-an-ecommerce-website/)
> **Stack:** Django REST Framework (backend) + React SPA (frontend)
> **Purpose:** Personal learning log — concepts, decisions, and code structure explained section by section.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Section 1 — Project Setup & Frontend Scaffold](#section-1--project-setup--frontend-scaffold)
- [Section 2 — Product Listing & Rating Component](#section-2--product-listing--rating-component)

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

## Section 2 — Product Listing & Rating Component

### What was built

The homepage product grid and reusable product card with star rating display.

**Files created:**
- `frontend/src/products.js` — hardcoded product data (temporary, replaced by Django API later)
- `frontend/src/pages/HomeScreen.jsx` — homepage, renders the product grid
- `frontend/src/components/Product.jsx` — single product card component
- `frontend/src/components/Rating.jsx` — reusable star rating display component

**Files updated:**
- `frontend/src/App.js` — now renders `<HomeScreen>` in the main body

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

*More sections will be added as the course progresses.*
