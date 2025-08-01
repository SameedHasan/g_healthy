import React, { useState, useRef, useEffect } from 'react'
import { SearchIcon } from '../../utils/icons'
import { Button, Input } from 'antd'

const Search = () => {
  const [expanded, setExpanded] = useState(false);
  const [value, setValue] = useState('');
  const inputRef = useRef(null);

  useEffect(() => {
    if (expanded && inputRef.current) {
      inputRef.current.focus();
    }
  }, [expanded]);

  const handleButtonClick = () => {
    if (!expanded) {
      setExpanded(true);
    } else if (value.trim() === '') {
      setExpanded(false);
    } else {
      // Trigger search logic here
      console.log('Searching for:', value);
    }
  };

  return (
    <div style={{ display: 'flex', alignItems: 'center', position: 'relative' }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        flexDirection: 'row',
      }}>
        <div style={{
          width: expanded ? 240 : 0,
          transition: 'width 0.3s',
          overflow: 'hidden',
          marginRight: expanded ? -25 : 0,
        }}>
          <Input
            ref={inputRef}
            type="text"
            value={value}
            onChange={e => setValue(e.target.value)}
            placeholder="Search..."
            style={{
              width: '100%',
              border: 'none',
              outline: 'none',
              borderRadius: "30px 0 0 30px",
              background: 'white',
              paddingLeft: 16,
              paddingRight: 32,
              transition: 'opacity 0.3s',
              opacity: expanded ? 1 : 0,
              boxShadow: '0px 1px 2px 0px rgba(0, 0, 0, 0.10)',
            }}
            onClick={e => e.stopPropagation()}
            onKeyDown={e => {
              if (e.key === 'Enter' && value.trim() !== '') {
                console.log('Searching for:', value);
              }
            }}
            tabIndex={expanded ? 0 : -1}
            disabled={!expanded}
          />
        </div>
        <Button
          icon={<SearchIcon />}
          color="default"
          variant="solid"
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
          onClick={handleButtonClick}
        />
      </div>
    </div>
  )
}

export default Search

