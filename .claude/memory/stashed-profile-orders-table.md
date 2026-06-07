---
name: stashed-profile-orders-table
description: Stashed ProfileScreen "My Orders" table render — reapply after user confirms orderListMy populates
metadata:
  type: project
---

The user wanted to first verify that visiting `/profile` populates `orderListMy` in Redux DevTools (they had never actually navigated to the profile page before — that's why orders looked "empty"). So my render changes were reverted and stashed here to reapply once confirmed.

The order DATA and fetch were always working: 9 orders exist in the DB on user 1 (`guillaume@gmail.com`), and `/api/orders/myorders/` returns all 9 with status 200. The only missing piece was rendering them on the profile page.

To reapply, in `frontend/src/pages/ProfileScreen.jsx`:

1. Imports — add `Table` to the react-bootstrap import and add `LinkContainer`:
```jsx
import { Form, Button, Col, Row, Table } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
```
(`react-router-bootstrap` is already installed.)

2. After the `userUpdateProfile` selector, add:
```jsx
const orderListMy = useSelector((state) => state.orderListMy);
const { loading: loadingOrders, error: errorOrders, orders } = orderListMy;
```

3. Replace the `<Col md={9}><h2>My Orders</h2></Col>` block with:
```jsx
<Col md={9}>
  <h2>My Orders</h2>
  {loadingOrders ? (
    <Loader />
  ) : errorOrders ? (
    <Message variant="danger">{errorOrders}</Message>
  ) : (
    <Table striped responsive className="table-sm">
      <thead>
        <tr>
          <th>ID</th>
          <th>Date</th>
          <th>Total</th>
          <th>Paid</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {orders.map((order) => (
          <tr key={order._id}>
            <td>{order._id}</td>
            <td>{order.createdAt.substring(0, 10)}</td>
            <td>${order.totalPrice}</td>
            <td>
              {order.isPaid ? (
                order.paidAt.substring(0, 10)
              ) : (
                <i className="fas fa-times" style={{ color: "red" }}></i>
              )}
            </td>
            <td>
              <LinkContainer to={`/order/${order._id}`}>
                <Button className="btn-sm">Details</Button>
              </LinkContainer>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  )}
</Col>
```

Note: the `orderListMyReducer` initial state was also fixed by the user from `{order: []}` (singular typo) to `{orders: []}` — keep that fix; the table's `orders.map` relies on it.
