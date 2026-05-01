import { legacy_createStore as createStore, combineReducers, applyMiddleware } from 'redux';
import { thunk } from 'redux-thunk';
import { composeWithDevTools } from '@redux-devtools/extension'
import { productListReducers, productDetailsReducers } from './reducers/productReducers.js'
import { cartReducer } from './reducers/cartReducers.js'
import { userLoginReducers, userRegisterReducers } from './reducers/userReducers.js';

const reducer = combineReducers({
    productList: productListReducers,
    productDetails: productDetailsReducers,
    cart: cartReducer,
    userLogin: userLoginReducers,
    userRegister: userRegisterReducers
})

const cartItemsFromStorage = localStorage.getItem('cartItems') ?
JSON.parse(localStorage.getItem('cartItems')) : []


const userInfoFromStorage = localStorage.getItem('userInfo') ?
JSON.parse(localStorage.getItem('userInfo')) : null

const initialState = {
    productList: { products: [] },
    cart: {cartItems: cartItemsFromStorage},
    userLogin: {userInfo: userInfoFromStorage}
}

const middleware = [thunk]

const store = createStore(
    reducer,
    initialState,
    composeWithDevTools(applyMiddleware(...middleware))
)

export default store