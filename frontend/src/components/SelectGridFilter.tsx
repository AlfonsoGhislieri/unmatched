import { Search } from './Search';

interface Props {
  // eslint-disable-next-line no-unused-vars
  onFilterChange: (query: string) => void;
}

function SelectGridFilter(props: Props) {
  props;
  return <Search onSearch={props.onFilterChange} />;
}

export { SelectGridFilter };
