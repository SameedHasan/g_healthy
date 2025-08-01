import React, { useState } from "react";
import {
  Input,
  Select,
  Upload,
  Button,
  Typography,
  Space,
  Divider,
} from "antd";
import { UploadOutlined, DownOutlined, PictureOutlined } from "@ant-design/icons";
import { Dropdown } from "antd";
import TiptapEditor from "../utility/TiptapEditor";
import TextArea from "antd/es/input/TextArea";
import DynamicModal from "../modals/DynamicModal";
import { MediaIcon, UploadIcon } from "../../utils/icons";

const { Title, label } = Typography;
const { Option } = Select;

const ArticleFormContent = ({ initialData = {}, onChange }) => {
  const [form, setForm] = useState({
    title: initialData.title || "",
    author: initialData.author || "",
    cover: initialData.cover || null,
    category: initialData.category || "",
    tags: initialData.tags ? initialData.tags.split(", ") : [],
    content: initialData.content || "",
  });
  const [mediaModalVisible, setMediaModalVisible] = useState(false);
  const uploadRef = React.useRef();

  const handleChange = (name, value) => {
    const updatedForm = { ...form, [name]: value };
    setForm(updatedForm);
    if (onChange) {
      onChange(updatedForm);
    }
  };

  const handleMenuClick = ({ key }) => {
    if (key === "media") {
      setMediaModalVisible(true);
    } else if (key === "upload") {
      // Trigger the Upload component's file dialog
      if (uploadRef.current) {
        uploadRef.current.click();
      }
    }
  };

  const items = [
    {
      key: "media",
      icon: <MediaIcon size={20}  />,
      label: "Choose from Media",
    },
    {
      key: "upload",
      icon: <UploadIcon/>,
      label: "Upload File",
    },
  ];

  return (
    <>
      <div className="form-section">
        <div className="form-section-item">
          <label htmlFor="title">Title</label>
          <Input
            id="title"
            placeholder="Title..."
            value={form.title}
            onChange={(e) => handleChange("title", e.target.value)}
          />
        </div>

        <div className="form-section-item">
          <label htmlFor="author">Author</label>
          <Input
            id="author"
            placeholder="Coach Jenny"
            value={form.author}
            onChange={(e) => handleChange("author", e.target.value)}
          />
        </div>

        <div className="form-section-item">
          <label>Article cover</label>
          <Upload
            name="cover"
            listType="picture-card"
            maxCount={1}
            className="modal-image-upload"
            showUploadList={false}
            beforeUpload={() => false} // prevent auto upload
            openFileDialogOnClick={false}
            style={{ width: '100%' }}
          >
            <div className="modal-image-upload-content" style={{ pointerEvents: 'none' }}>
              <h3>
                Drop images here <span>or</span>
              </h3>
              {/* Only the dropdown button is interactive */}
              <span style={{ pointerEvents: 'auto' }}>
                <Dropdown
                  menu={{ items, onClick: handleMenuClick }}
                  trigger={["click"]}
                  placement="bottom"
                >
                  <Button className="btn-sm" color="primary" variant="outlined" style={{ display: 'flex', alignItems: 'center' }}>
                    Browse
                  </Button>
                </Dropdown>
              </span>
              <input
                type="file"
                ref={uploadRef}
                style={{ display: "none" }}
                onChange={e => {
                  if (e.target.files && e.target.files[0]) {
                    handleChange("cover", e.target.files[0]);
                  }
                }}
              />
              <p>MP4, MOV and AVI up to 30 MB</p>
            </div>
          </Upload>
          {/* Media selection modal */}
          <DynamicModal
            visible={mediaModalVisible}
            onCancel={() => setMediaModalVisible(false)}
            title="Choose from Media"
            width={770}
            footerButtons={[
              <Button key="close"  type="primary" onClick={() => setMediaModalVisible(false)}>Choose</Button>
            ]}
          >
            {/* TODO: Media picker content goes here */}
            <div style={{ minHeight: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#888' }}>
              Media picker goes here
            </div>
          </DynamicModal>
        </div>

        <div className="form-section-item">
          <label>Category</label>
          <Select
            placeholder="Select category"
            style={{ width: "100%", marginTop: 8 }}
            value={form.category || undefined}
            onChange={(value) => handleChange("category", value)}
          >
            <Option value="Lifestyle">Lifestyle</Option>
            <Option value="Coaching">Coaching</Option>
            <Option value="Health Tips">Health Tips</Option>
            <Option value="Nutrition">Nutrition</Option>
          </Select>
        </div>

        <div className="form-section-item">
          <label>Tags</label>
          <Select
            mode="tags"
            placeholder="Add tags..."
            style={{ width: "100%", marginTop: 8 }}
            value={form.tags}
            onChange={(value) => handleChange("tags", value)}
          >
            <Option value="kids">kids</Option>
            <Option value="activity">activity</Option>
            <Option value="fitness">fitness</Option>
            <Option value="goal-setting">goal-setting</Option>
            <Option value="progress">progress</Option>
            <Option value="tips">tips</Option>
          </Select>
        </div>
      </div>

      <div className="form-section">
        <div className="form-section-item-title">
          <h3>Content</h3>
          <p>What needs to be done to mark the lesson as complete</p>
        </div>
        <div className="form-section-item">
          <TiptapEditor
            content={form.content}
            onChange={(value) => handleChange("content", value)}
          />
        </div>

        <div className="form-section-item">
          <label>Excerpt (optional short summary)</label>
          <TextArea
            rows={2}
            placeholder="Excerpt..."
            value={form.author}
            onChange={(e) => handleChange("author", e.target.value)}
          />
        </div>
      </div>
    </>
  );
};

export default ArticleFormContent;
