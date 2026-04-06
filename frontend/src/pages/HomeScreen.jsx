import React from "react";
import products from "./../products.js";
import { Row, Col } from "react-bootstrap";
import Product from "../components/Product";

export default function HomeScreen() {
  return (
    <div>
      <h1>Latest Product</h1>
      <Row>
        {products.map((p) => (
          <Col sm={12} md={6} lg={4} xl={3} key={p._id}>
            <Product product={p}/>
          </Col>
        ))}
      </Row>
    </div>
  );
}
