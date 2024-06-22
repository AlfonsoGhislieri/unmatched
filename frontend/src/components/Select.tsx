import { useState } from 'react';

interface SelectProps {
  name: string;
  hoverable?: boolean;
  onClick?: () => void;
}

function Select(props: SelectProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);

  let cardImgPath, miniImgPath;

  try {
    // eslint-disable-next-line no-undef
    cardImgPath = require(`../assets/select/cards/${props.name}.webp`);
    // eslint-disable-next-line no-undef
    miniImgPath = require(`../assets/select/minis/${props.name}.webp`);
  } catch (error) {
    console.error('Image not found:', error);
    return <div>Image not found</div>;
  }

  return (
    <div
      id={`select-${props.name}`}
      className={`select
        ${props.hoverable && (isHovered || isAnimating) ? 'hovered' : ''}
      `}
      onMouseEnter={() => {
        setIsHovered(true);
        setIsAnimating(true);
      }}
      onMouseLeave={() => setIsHovered(false)}
      onTransitionEnd={() => setTimeout(() => setIsAnimating(false), 100)}
      onClick={props.onClick}
    >
      <img src={cardImgPath} alt={props.name} className='card-img' />
      <img src={miniImgPath} alt={props.name} className='mini-img' />
    </div>
  );
}

export { Select };
