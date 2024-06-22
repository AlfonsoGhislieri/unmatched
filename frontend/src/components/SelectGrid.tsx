import { HeroPageModal } from './HeroPageModal';
import { Select } from './Select';
import { isElementInViewport } from 'utils/viewportUtils';
import { useState } from 'react';

const msFlipCascadeDelay = 50;

interface SelectGridProps {
  heroes: string[];
}

function SelectGrid(props: SelectGridProps) {
  const [openingModal, setOpeningModal] = useState(false);
  const [selectedId, setSelectedId] = useState('');

  const handleSelectClick = (target: string) => {
    animateCascadingFlipRecursive(0, target);
  };

  const animateCascadingFlipRecursive = (id: number, target: string) => {
    if (id == props.heroes.length) {
      setOpeningModal(false);
      setTimeout(() => setSelectedId(target), 250);
      return;
    }
    const selectElement = document.getElementById(`select-${props.heroes[id]}`);
    const delay = isElementInViewport(selectElement) ? msFlipCascadeDelay : 0;
    setTimeout(() => {
      if (props.heroes[id] != target) selectElement?.classList.add('flip');
      animateCascadingFlipRecursive(id + 1, target);
    }, delay);
  };

  return selectedId != '' ? (
    <div>
      <HeroPageModal name={selectedId} onClick={() => null} />
      <button onClick={() => setSelectedId('')}>Close</button>
    </div>
  ) : (
    <div className='select-grid'>
      {props.heroes.map((hero: string) => (
        <Select key={hero} name={hero} hoverable={!openingModal} onClick={() => handleSelectClick(hero)} />
      ))}
    </div>
  );
}

const allHeroes = [
  'Achilles',
  'Alice',
  'Angel',
  'AnnieChristmas',
  'Beowulf',
  'Bigfoot',
  'BlackPanther',
  'BlackWidow',
  'BloodyMary',
  'BruceLee',
  'Buffy',
  'Bullseye',
  'CloakAndDagger',
  'Daredevil',
  'Deadpool',
  'Dracula',
  'DrSattler',
  'DoctorStrange',
  'Elektra',
  'GhostRider',
  'GoldenBat',
  'Hamlet',
  'Houdini',
  'InGen',
  'InvisibleMan',
  'JekyllAndHyde',
  'JillTrent',
  'KingArthur',
  'LittleRed',
  'LukeCage',
  'Medusa',
  'MoonKnight',
  'MsMarvel',
  'NikolaTesla',
  'OdaNobunaga',
  'Raptors',
  'RobinHood',
  'Shakespeare',
  'SheHulk',
  'SherlockHolmes',
  'Sinbad',
  'SpiderMan',
  'Spike',
  'SquirrelGirl',
  'SunWukong',
  'Titania',
  'TheGenie',
  'TomoeGozen',
  'TRex',
  'WaywardSisters',
  'Willow',
  'WinterSoldier',
  'Yennenga',
];

export { SelectGrid, allHeroes };
