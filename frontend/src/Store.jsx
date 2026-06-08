import { legacy_createStore as createStore, combineReducers, applyMiddleware } from 'redux';
import { thunk } from 'redux-thunk';
import { composeWithDevTools } from '@redux-devtools/extension'
import { productListReducers, productDetailsReducers } from './reducers/productReducers.js'
import { cartReducer } from './reducers/cartReducers.js'
import { userLoginReducers, userRegisterReducers, userDetailsReducers, userUpdateProfileReducers, userListReducers, userDeleteReducers, userUpdateReducers } from './reducers/userReducers.js';
import { orderCreateReducer, orderDetailsReducer, orderListMyReducer, orderPayReducer } from './reducers/orderReducers.js'

const reducer = combineReducers({
    productList: productListReducers,
    productDetails: productDetailsReducers,
    cart: cartReducer,
    userLogin: userLoginReducers,
    userRegister: userRegisterReducers,
    userDetails: userDetailsReducers,
    userUpdateProfile: userUpdateProfileReducers,
    userList: userListReducers,
    userDelete: userDeleteReducers,
    orderCreate: orderCreateReducer,
    orderDetails: orderDetailsReducer,
    orderPay: orderPayReducer,
    orderListMy: orderListMyReducer,
    userUpdate: userUpdateReducers,
})

const cartItemsFromStorage = localStorage.getItem('cartItems') ?
JSON.parse(localStorage.getItem('cartItems')) : []


const userInfoFromStorage = localStorage.getItem('userInfo') ?
JSON.parse(localStorage.getItem('userInfo')) : null

const shippingAddressFromStorage = localStorage.getItem('shippingAddress') ?
JSON.parse(localStorage.getItem('shippingAddress')) : {}

const initialState = {
    productList: { products: [] },
    cart: {cartItems: cartItemsFromStorage, shippingAddress:  shippingAddressFromStorage},
    userLogin: {userInfo: userInfoFromStorage}
}

const middleware = [thunk]

const store = createStore(
    reducer,
    initialState,
    composeWithDevTools(applyMiddleware(...middleware))
)

export default store