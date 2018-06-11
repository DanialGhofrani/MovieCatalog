// index.jsx
import React from 'react';
import ReactDOM from 'react-dom';
import Wrapper from './components/wrapper';
import { createStore, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';
import { createLogger } from 'redux-logger';
import movieCatalogue from './reducers';

const loggerMiddleWear = createLogger();

const store = createStore(
  movieCatalogue,
  applyMiddleware(thunkMiddleware, loggerMiddleWear)
);
const render = () =>
  ReactDOM.render(
    <Wrapper reduxStore={store} />,
    document.getElementById('content')
  );

render();
store.subscribe(render);
