import React from "react";
import { Typography, Space, Tag, Divider, Dropdown, Button } from "antd";
import { CheckCircleIcon, ThreeDotIcon } from "../../utils/icons";

const { Title, Text, Paragraph } = Typography;

export const getActionItems = () => {
  return [
    {
      key: "edit",
      label: "Edit",
    },
    {
      key: "delete",
      label: "Delete",
      danger: true,
    },
  ];
};



const ArticleDetailContent = ({ article }) => {
  if (!article) return null;

  return (
    <div className="custom-drawer">
      <div className="title">
        <div>
          <h1>{article.title || "No Title"}</h1>
        </div>
        <div className="actions">
          <Tag className="title-tag" color="green">
            Published
          </Tag>
          <Dropdown arrow overlayClassName="action-dropdown" menu={{ items: getActionItems(article) }} trigger={["click"]}>
            <Button className="atn-btn action-btn" type="text" icon={<ThreeDotIcon />} />
          </Dropdown>
        </div>
      </div>

      <div className="info">
        <div className="info-item">
          <div className="info-item-title">
            <h3>Short description</h3>
          </div>
          <div className="info-item-description">
            <p>{article.content || "Example description here lorem ipsum dolor sit amet la, text funding campaign here ipsum pasum."}</p>
          </div>
        </div>
        <div className="info-item">
          <div className="info-item-title">
            <h3>Author</h3>
          </div>
          <div className="info-item-description">
            <p>{article.author}</p>
          </div>
        </div>
        <div className="info-item">
          <div className="info-item-title">
            <h3>Publish Date</h3>
          </div>
          <div className="info-item-description">
            <p>{article.datePublished}</p>
          </div>
        </div>

        <div className="info-item">
          <div className="info-item-title">
            <h3 strong>Article cover</h3>
          </div>
          <div className="info-item-description">
            <p>
              {article.cover ? (
                <img src={article.cover} alt="Article cover" style={{ maxWidth: "100%", marginTop: 8 }} />
              ) : (
                <p type="secondary">No cover image</p>
              )}
            </p>
          </div>
        </div>

        <div className="info-item">
          <div className="info-item-title">
            <h3>Category</h3>
          </div>
          <div className="info-item-description">
            <p>{article.category}</p>
          </div>
        </div>
        <div className="info-item">
          <div className="info-item-title">
            <h3>Tags</h3>
          </div>
          <div className="info-item-description">
            <p>
              {article.tags &&
                article.tags.split(", ").map((tag, index, arr) => (
                  <span key={tag}>
                    {tag}
                    {index < arr.length - 1 && ", "}
                  </span>
                ))}
            </p>
          </div>
        </div>
      </div>
      <div>
        <Divider />
      </div>
      <div className="info">
        <h2 className="info-heading">Content</h2>
        <div className="text-editor">
          <div className="section">
            <h4>1. Why Movement Matters</h4>
            <div className="content-text">
              <p>Staying active isn't just about exercise—it's about keeping your body moving throughout the day. Regular movement helps:</p>
              <div className="bullet-point">
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p> Boost energy levels and reduce tiredness.</p>
                </div>
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p> Improve focus and mood, making you feel happier.</p>
                </div>
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p> Strengthen your muscles, bones, and heart for long-term health.</p>
                </div>
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p> Support healthy weight management and overall wellness.</p>
                </div>
              </div>
            </div>
          </div>
          <div className="section">
            <h4>2. Ways to Stay Active</h4>
            <div className="content-text">
              <p>You don't need a gym to be active—movement can be part of your daily routine!</p>
              <h6>Move Your Body Every Day</h6>
              <div className="bullet-point">
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p> Take a 10-minute walk after meals.</p>
                </div>
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p> Dance to your favorite music for a quick energy boost.</p>
                </div>
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p> Stretch for 5 minutes in the morning or before bed.</p>
                </div>
              </div>
              <h6>Make it Fun!</h6>
              <div className="bullet-point">
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p>Try a movement challenge (jump rope, hula hoop, or step count).</p>
                </div>
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p>Set a goal with a friend or family member.</p>
                </div>
                <div className="custom-li">
                  <CheckCircleIcon />
                  <p> Join a sports or activity class you enjoy</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="info-item">
          <div className="info-item-title">
            <h3>Excerpt (optional short summary)</h3>
          </div>
          <div className="info-item-description">
            <p>Staying active isn’t just about exercise—it’s about keeping your body moving throughout the day. Regular movement helps:</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleDetailContent;
