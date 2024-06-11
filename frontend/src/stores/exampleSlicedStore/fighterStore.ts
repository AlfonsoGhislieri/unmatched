// @ts-nocheck
import { create } from 'zustand';
import { combine } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

// Splitting out a store into slices
// https://github.com/pmndrs/zustand/blob/HEAD/docs/guides/slices-pattern.md

// @ts-ignore
const createCartSlice = (set) => ({
  cart: [],
  addToCart: (product) =>
    set((state) => {
      state.cart.push(product);
    }),
});

const createProductSlice = (set) => ({
  products: [],
  setProducts: (products) =>
    set((state) => {
      state.products = products;
    }),
});

const createUserSlice = (set) => ({
  user: null,
  setUser: (user) =>
    set((state) => {
      state.user = user;
    }),
});

// Combine slices into a single store
const useStore = create(
  immer(
    combine({
      ...createCartSlice,
      ...createProductSlice,
      ...createUserSlice,
    })
  )
);

export default useStore;
