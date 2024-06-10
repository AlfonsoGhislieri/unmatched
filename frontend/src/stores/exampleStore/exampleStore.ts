import { create } from 'zustand';
import { combine, devtools } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

// https://github.com/pmndrs/zustand/blob/HEAD/docs/guides/typescript.md
interface Person {
  name: string;
  age: number;
}

const useExampleStore = create(
  devtools(
    immer(
      combine(
        {
          people: [] as Person[],
        },
        (set) => ({
          add(name: string, age: number) {
            set((state) => {
              state.people.push({ name, age });
            });
          },
          remove(name: string) {
            set((state) => {
              state.people = state.people.filter((p) => p.name !== name);
            });
          },
        })
      )
    ),
    { name: 'ExampleStore' }
  )
);

export default useExampleStore;
