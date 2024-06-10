import React from 'react';
import useExampleStore from './stores/exampleStore/exampleStore';
import useStore from 'stores/exampleSlicedStore/fighterStore';

const PeopleList: React.FC = () => {
  const people = useExampleStore((state) => state.people);
  const add = useExampleStore((state) => state.add);
  const remove = useExampleStore((state) => state.remove);

  const handleAdd = () => {
    const name = prompt('Enter name:');
    const age = parseInt(prompt('Enter age:') || '0', 10);
    if (name) {
      add(name, age);
    }
  };

  const handleRemove = (name: string) => {
    remove(name);
  };

  return (
    <div>
      <h1>People List</h1>
      <button onClick={handleAdd}>Add Person</button>
      <ul>
        {people.map((person) => (
          <li key={person.name}>
            {person.name} ({person.age} years old)
            <button onClick={() => handleRemove(person.name)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PeopleList;
