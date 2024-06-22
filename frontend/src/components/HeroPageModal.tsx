import { Select } from './Select';

interface HeroPageModalProps {
  name: string;
  onClick: () => void;
}

function HeroPageModal(props: HeroPageModalProps) {
  return (
    <div className='hero-page-modal'>
      <Select name={props.name} hoverable={false} onClick={props.onClick} />
    </div>
  );
}

export { HeroPageModal };
