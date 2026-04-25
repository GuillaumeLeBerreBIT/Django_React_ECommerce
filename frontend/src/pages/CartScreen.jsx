import React, { useEffect } from "react";
import {
  Link,
  useLocation,
  useSearchParams,
  useNavigate,
  useParams,
} from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import {
  Row,
  Col,
  ListGroup,
  Form,
  Button,
  Card,
  Image,
} from "react-bootstrap";
import Message from "../components/Message";
import { addToCart, removeFromCart } from "../actions/cartActions";

export default function CartScreen() {
  const { id } = useParams();
  const navigate = useNavigate();
  // const location = useLocation()
  // const qty = location.search ? Number(location.search.split('=')[1]) : 1
  const [searchParams] = useSearchParams();
  const qty = Number(searchParams.get("qty")) || 1;
  console.log(qty);
  const dispatch = useDispatch();

  const cart = useSelector((state) => state.cart);
  const { cartItems } = cart;
  console.log(cartItems);

  useEffect(() => {
    if (id) {
      dispatch(addToCart(id, qty));
    }
  }, [dispatch, id, qty]);

  function removeFromCartHandler (id) {
    dispatch(removeFromCart(id))
  }

  function checkoutHandler () {
    navigate('/login?redirect=shipping')
  }

  return (
    <Row>
      <Col md={8}>
        <h1>Shopping Cart</h1>
        {cartItems.length === 0 ? (
          <Message variant="info">
            Your cart is empty <Link to="/">Go Back</Link>
          </Message>
        ) : (
          <ListGroup>
            {cartItems.map((item) => (
              <ListGroup.Item
                key={item.product}
                variant="flush"
              >
                <Row>
                  <Col md={2}>
                    <Image src={item.image} alt={item.name} fluid rounded />
                  </Col>
                  <Col md={3}>
                    <Link to={`/product/${item.product}`}>{item.name}</Link>
                  </Col>
                  <Col md={2}>${item.price}</Col>

                  <Col md={3}>
                    <Form.Control
                      as="select"
                      value={item.qty}
                      onChange={(e) => {
                        dispatch(addToCart(item.product, Number(e.target.value)));
                      }}
                    >
                      {[...Array(item.countInStock).keys()].map((x) => (
                        <option key={x + 1} value={x + 1}>
                          {x + 1}
                        </option>
                      ))}
                    </Form.Control>
                  </Col>
                  <Col md={1}>
                    <Button type="button" variant="light" onClick={() => removeFromCartHandler(item.product)}>
                      
                      <i className="fas fa-trash"></i>
                    </Button>
                  </Col>
                </Row>
              </ListGroup.Item>
            ))}
          </ListGroup>
        )}
      </Col>

      <Col md={4}>
        <Card>
            <ListGroup variant="flush">
                <ListGroup.Item>
                    <h2>Subtotal ({cartItems.reduce((acc, item) => acc + (item.qty), 0)})</h2>
                    ${cartItems.reduce((acc, item) => acc + (item.price * item.qty), 0).toFixed(2)}
                </ListGroup.Item>

                <ListGroup.Item>
                    <Button type="button" className="btn-block"
                    disabled={true && (cartItems.length === 0)}
                    onClick={checkoutHandler}>
                        Proceed to Checkout
                    </Button>
                </ListGroup.Item>
            </ListGroup>
        </Card>
      </Col>
    </Row>
  );
}
