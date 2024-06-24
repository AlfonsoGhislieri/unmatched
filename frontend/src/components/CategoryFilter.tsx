import { useEffect, useState } from 'react';

interface CategoryFilterProps {
  title: string;
  categories: string[];
  // eslint-disable-next-line no-unused-vars
  onChange: (category: string[]) => void;
}

function CategoryFilter(props: CategoryFilterProps) {
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const handleSelectedChange = (category: string) => {
    const updatedSelected = new Set(selected);
    if (updatedSelected.has(category)) updatedSelected.delete(category);
    else updatedSelected.add(category);
    setSelected(updatedSelected);
  };

  useEffect(() => {
    props.onChange(Array.from(selected));
  }, [selected]);

  return (
    <div>
      {props.title}:
      <br />
      {props.categories.map((category) => (
        <label key={category}>
          <input type='checkbox' checked={selected.has(category)} onChange={() => handleSelectedChange(category)} />
          {category}
        </label>
      ))}
    </div>
  );
}

export { CategoryFilter };
