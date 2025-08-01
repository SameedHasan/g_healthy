import React, { useRef, useState } from 'react';
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import TaskList from '@tiptap/extension-task-list';
import TaskItem from '@tiptap/extension-task-item';
import Underline from '@tiptap/extension-underline';
import Link from '@tiptap/extension-link';
import Image from '@tiptap/extension-image';
import { Table } from '@tiptap/extension-table';
import { TableRow } from '@tiptap/extension-table-row';
import { TableCell } from '@tiptap/extension-table-cell';
import { TableHeader } from '@tiptap/extension-table-header';
import { BoldIcon, ItalicIcon, ListIcon, ListSettingsIcon, StrikeIcon, UnderlineIcon, LinkIcon, AttachmentIcon, TableCellsIcon, MediaIcon, UploadIcon } from '../../utils/icons';
import DynamicModal from '../modals/DynamicModal';
import { Node, mergeAttributes } from '@tiptap/core';
import { Button, Dropdown, Input, Menu } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

// Improved custom video extension
const Video = Node.create({
  name: 'video',
  group: 'block',
  atom: true,
  selectable: true,
  draggable: true,
  addAttributes() {
    return {
      src: { default: null },
      controls: { default: true },
      style: { default: 'max-width:100%;' },
    };
  },
  parseHTML() {
    return [
      {
        tag: 'video',
      },
    ];
  },
  renderHTML({ HTMLAttributes }) {
    return ['video', mergeAttributes(HTMLAttributes)];
  },
});

export default function TiptapEditor({ content, onChange }) {
  const fileInputRef = useRef();
  const [linkModalVisible, setLinkModalVisible] = useState(false);
  const [linkInput, setLinkInput] = useState('');
  const editor = useEditor({
    extensions: [
      StarterKit.configure({
        orderedList: false, // Disable default ordered list
      }),
      TaskList,
      TaskItem,
      Underline,
      Link.extend({
        addAttributes() {
          return {
            ...this.parent?.(),
            title: {
              default: null,
              parseHTML: element => element.getAttribute('title'),
              renderHTML: attributes => {
                return {
                  title: attributes.href || null,
                };
              },
            },
          };
        },
      }).configure({
        openOnClick: true,
        autolink: false,
        linkOnPaste: true,
      }),
      Image,
      Video,
      Table.configure({ resizable: true }),
      TableRow,
      TableCell,
      TableHeader,
    ],
    content: content || '',
    onUpdate: ({ editor }) => {
      if (onChange) onChange(editor.getHTML());
    },
  });

  if (!editor) {
    return null;
  }

  // Link handler
  const setLink = () => {
    const previousUrl = editor.getAttributes('link').href;
    setLinkInput(previousUrl || '');
    setLinkModalVisible(true);
  };
  const handleLinkSubmit = () => {
    if (linkInput === '') {
      editor.chain().focus().extendMarkRange('link').unsetLink().run();
    } else {
      editor.chain().focus().extendMarkRange('link').setLink({ href: linkInput, title: linkInput }).run();
    }
    setLinkModalVisible(false);
  };

  // Attachment handler
  const handleAttachmentClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
      fileInputRef.current.click();
    }
  };
  const handleFileChange = (e) => {
    const file = e.target.files && e.target.files[0];
    if (file) {
      const url = URL.createObjectURL(file);
      const ext = file.name.split('.').pop().toLowerCase();
      if (["png", "jpg", "jpeg", "gif", "webp", "bmp", "svg"].includes(ext)) {
        // Insert image
        editor.chain().focus().setImage({ src: url, alt: file.name }).run();
      } else if (["mp4", "webm", "ogg", "mov", "avi", "mkv"].includes(ext)) {
        // Insert video
        editor.chain().focus().insertContent({
          type: 'video',
          attrs: { src: url, controls: true, style: 'max-width:100%;' },
        }).run();
      } else {
        // Insert as link
        editor.chain().focus().insertContent(`<a href="${url}" target="_blank">${file.name}</a>`).run();
      }
    }
  };

  // Dropdown menu for attachment
  const attachmentMenuItems = [
    {
      key: 'media',
      icon: <MediaIcon size={20} />, // You can use a different icon if you want
      label: 'Choose from Media',
    },
    {
      key: 'upload',
      icon: <UploadIcon />, // Use Ant Design's upload icon
      label: 'Upload File',
    },
  ];
  const handleAttachmentMenuClick = ({ key }) => {
    if (key === 'media') {
      // Open your media modal (reuse linkModalVisible or add a new state if needed)
      setMediaModalVisible(true);
    } else if (key === 'upload') {
      handleAttachmentClick();
    }
  };
  // Add state for media modal if not present
  const [mediaModalVisible, setMediaModalVisible] = useState(false);
  const [attachmentDropdownOpen, setAttachmentDropdownOpen] = useState(false);

  // Custom resize logic for the grip
  const editorRef = useRef();
  const gripRef = useRef();
  React.useEffect(() => {
    const grip = gripRef.current;
    const editorEl = editorRef.current?.querySelector('.ProseMirror');
    if (!grip || !editorEl) return;
    let startY = 0;
    let startHeight = 0;
    let dragging = false;
    const minHeight = 120;
    const maxHeight = 600;
    function onMouseDown(e) {
      dragging = true;
      startY = e.clientY;
      startHeight = parseInt(window.getComputedStyle(editorEl).height, 10);
      document.body.style.userSelect = 'none';
    }
    function onMouseMove(e) {
      if (!dragging) return;
      const dy = e.clientY - startY;
      let newHeight = startHeight + dy;
      newHeight = Math.max(minHeight, Math.min(maxHeight, newHeight));
      editorEl.style.height = newHeight + 'px';
    }
    function onMouseUp() {
      dragging = false;
      document.body.style.userSelect = '';
    }
    grip.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    return () => {
      grip.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };
  }, [editor]);

  return (
    <div className="tiptap-editor">
      {/* Toolbar */}
      <div className="tiptap-toolbar" >
        <div className="section">
          <button onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()} className={`h1 ${editor.isActive('heading', { level: 1 }) ? 'is-active' : ''}`}>H1</button>
          <button onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()} className={`h2 ${editor.isActive('heading', { level: 2 }) ? 'is-active' : ''}`}>H2</button>
          <button onClick={() => editor.chain().focus().setParagraph().run()} className={editor.isActive('paragraph') ? 'is-active' : ''}>Body</button>
        </div>
        <div className="toolbar-divider" />
        <div className="section">
          <button onClick={() => editor.chain().focus().toggleBold().run()} className={editor.isActive('bold') ? 'is-active' : ''}><BoldIcon /></button>
          <button onClick={() => editor.chain().focus().toggleItalic().run()} className={editor.isActive('italic') ? 'is-active' : ''}><ItalicIcon /></button>
          <button onClick={() => editor.chain().focus().toggleUnderline().run()} className={editor.isActive('underline') ? 'is-active' : ''}><UnderlineIcon /></button>
          <button onClick={() => editor.chain().focus().toggleStrike().run()} className={editor.isActive('strike') ? 'is-active' : ''}><StrikeIcon /></button>
        </div>
        <div className="toolbar-divider" />
        <div className="section">
          <button onClick={() => editor.chain().focus().toggleBulletList().run()} className={editor.isActive('bulletList') ? 'is-active' : ''}><ListIcon /></button>
          <button onClick={() => editor.chain().focus().toggleTaskList().run()} className={editor.isActive('taskList') ? 'is-active' : ''}><ListSettingsIcon /></button>
        </div>
        <div className="toolbar-divider" />
        <div className="section">
          <button onClick={setLink} className={editor.isActive('link') ? 'is-active' : ''}><LinkIcon /></button>
          <Dropdown
            menu={{ items: attachmentMenuItems, onClick: handleAttachmentMenuClick }}
            trigger={["click"]}
            placement="top"
            onOpenChange={setAttachmentDropdownOpen}
          >
            <span>
              <button
                type="button"
                className={`ant-btn ant-btn-icon${attachmentDropdownOpen ? ' is-active' : ''}`}
              >
                <AttachmentIcon color={attachmentDropdownOpen ? 'var(--color-text-base)' : '#616161'} />
              </button>
            </span>
          </Dropdown>
          <input type="file" ref={fileInputRef} style={{ display: 'none' }} onChange={handleFileChange} />
          {/* <button onClick={() => editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()} type="button"><TableCellsIcon /></button> */}
        </div>
        {/* <div className="toolbar-divider" /> */}
        {/*<div className="section">
         <button onClick={() => editor.chain().focus().addColumnBefore().run()} type="button">+Col</button>
           <button onClick={() => editor.chain().focus().addColumnAfter().run()} type="button">Col+</button>
          <button onClick={() => editor.chain().focus().deleteColumn().run()} type="button">-Col</button>
          <button onClick={() => editor.chain().focus().addRowBefore().run()} type="button">+Row</button>
          <button onClick={() => editor.chain().focus().addRowAfter().run()} type="button">Row+</button>
          <button onClick={() => editor.chain().focus().deleteRow().run()} type="button">-Row</button>
          <button onClick={() => editor.chain().focus().deleteTable().run()} type="button">Del Table</button>
        </div>*/}
      </div>
      {/* Link Modal */}
      <DynamicModal
        visible={linkModalVisible}
        onCancel={() => setLinkModalVisible(false)}
        title="Insert Link"
        width={650}
        className="link-modal"
        footerButtons={[
          <Button key="cancel" onClick={() => setLinkModalVisible(false)} >Cancel</Button>,
          <Button key="ok" onClick={handleLinkSubmit} type="primary" color="primary" >OK</Button>
        ]}
      >
        <div className="form-section">
          <div className="form-section-item">
            <label htmlFor="title">URL</label>
            <Input
              id="link-input"
              type="text"
              value={linkInput}
              onChange={e => setLinkInput(e.target.value)}
              placeholder="https://example.com"
              style={{ padding: 8, border: '1px solid #eee', borderRadius: 4 }}
            />
          </div>
        </div>

      </DynamicModal>
      {/* Media Modal for attachment dropdown */}
      <DynamicModal
        visible={mediaModalVisible}
        onCancel={() => setMediaModalVisible(false)}
        title="Choose from Media"
        className="media-modal"
        width={770}
        footerButtons={[
          <Button key="close" type="primary" onClick={() => setMediaModalVisible(false)}>Choose</Button>
        ]}
      >
        <div style={{ minHeight: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#888' }}>
          Media picker goes here
        </div>
      </DynamicModal>
      {/* Editor */}
      <div ref={editorRef}>
        <EditorContent editor={editor} />
        <div className="tiptap-resize-grip-container">
          <div className="tiptap-resize-grip" ref={gripRef} />
        </div>
      </div>
    </div>
  );
}
