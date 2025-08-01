import React, { useState } from "react";
import {
  Layout,
  Space,
  Button,
  Input,
  Typography,
  Upload,
  DatePicker,
  Select,
  Divider,
} from "antd";
import {
  SearchOutlined,
  ExportOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UploadOutlined,
  FilterOutlined,
  PlusOutlined,
  SortAscendingOutlined,
  CalendarOutlined,
  ReloadOutlined,
} from "@ant-design/icons";
import { useLocation } from "react-router-dom";
import DynamicModal from "../modals/DynamicModal";
import ArticleFormContent from "../content/ArticleFormContent";
import ExportFormContent from "../content/ExportFormContent";
import {
  AdjustIcon,
  CalendarIcon,
  PlusIcon,
  SearchIcon,
} from "../../utils/icons";
import SortTable from "../headerAction/SortTable";
import Search from "../headerAction/Search";
import CustomRangePicker from "../headerAction/CustomRangePicker";
import { useRoutesStore } from "../../store";

const { Header: AntHeader } = Layout;
const { Title } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

const Header = ({ collapsed, toggleSidebar, onSearch }) => {
  const location = useLocation();
  const pathname = location.pathname;
  const { getRouteByPath, getAllRoutes } = useRoutesStore();
  const allRoutes = getAllRoutes();
  let patharray = location.pathname.split("/")?.splice(1);
  const getCurrentRoute = () => {
    let currentRoute = null;
    allRoutes.forEach((i) => {
      if (i?.subRoutes && !currentRoute) {
        currentRoute = i?.subRoutes.find(
          (i) => i.path === patharray[patharray?.length - 1]
        );
      }
    });
    return currentRoute;
  };
  const currentRoute = getRouteByPath(pathname) || "No Title";

  const [modalVisible, setModalVisible] = useState(false);
  const [modalType, setModalType] = useState("add");
  const [searchText, setSearchText] = useState("");

  const handleOpenModal = (type) => {
    setModalType(type);
    setModalVisible(true);
  };

  const handleCloseModal = () => {
    setModalVisible(false);
  };

  const handleSearch = (e) => {
    const value = e.target.value;
    setSearchText(value);
    if (onSearch) {
      onSearch(value);
    }
  };

  const handleResetSearch = () => {
    setSearchText("");
    if (onSearch) {
      onSearch("");
    }
  };

  // Determine if search should be shown based on current path
  const shouldShowSearch = () => {
    return ["/goals", "/logs/goals", "/Lessons", "/media"].some(
      (path) => pathname === path || pathname.startsWith(path)
    );
  };
  return (
    <AntHeader className="custom-ant-header">
      <Space align="center">
        <Title
          level={1}
          style={{ margin: 0, fontSize: "32px", fontWeight: "700" }}
        >
          {currentRoute?.title || currentRoute?.label || "No title"}
        </Title>
      </Space>
      <Space size="middle">
        {/* Dashboard page - Date range picker */}
        {pathname === "/dashboard" ||
          (pathname === "/" && (
            <>
              <Search />
              <CustomRangePicker />
            </>
          ))}

        {/* Media page - Search input, Sort by, Filter, and Upload */}
        {pathname.startsWith("/media") && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />

            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Upload media"
              // onClick={() => handleOpenModal('upload')}
            >
              Upload
            </Button>
          </>
        )}

        {/* Goals page - Search input and Export */}
        {(pathname === "/goals" ||
          pathname === "/logs/goals" ||
          pathname === "/logs/weight" ||
          pathname === "/logs/activity" ||
          pathname === "/logs/kicks" ||
          pathname === "/logs/contractions") && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Export goals"
              // onClick={() => handleOpenModal('export')}
            >
              Export
            </Button>
          </>
        )}

        {/* community page - Search input and Export */}
        {(pathname === "/community" ||
          pathname === "/surveys" ||
          pathname === "/exercises" ||
          pathname === "/recipes" ||
          pathname === "/goals/nutritional" ||
          pathname === "/goals/activity" ||
          pathname === "/goals/behavioral") && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label={`Add ${
                pathname === "/surveys"
                  ? "Survey"
                  : pathname === "/exercises"
                  ? "Exercise"
                  : pathname === "/community"
                  ? "Goal"
                  : "Recipe"
              }`}
              // onClick={() => handleOpenModal('export')}
            >
              {pathname === "/surveys"
                ? "Add Survey"
                : pathname === "/exercises"
                ? "Add  Exercise"
                : pathname === "/community"
                ? "Export"
                : pathname === "/recipes"
                ? "Add  Recipe"
                : "Add  Goal"}
            </Button>
          </>
        )}

        {pathname === "/app-users" && (
          <>
            {/* <Input
              placeholder="Search goals..."
              prefix={<SearchOutlined />}
              onChange={handleSearch}
              value={searchText}
              style={{ width: 250 }}
              allowClear
            /> */}
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Export goals"
              // onClick={() => handleOpenModal('export')}
            >
              Export
            </Button>
          </>
        )}

        {pathname === "/Lessons" && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              onClick={() => handleOpenModal("add")}
            >
              Add Articles
            </Button>
          </>
        )}

        {/* Default search icon and export for other pages */}
        {![
          "/",
          "/dashboard",
          "/media",
          "/goals",
          "/logs/goals",
          "/Lessons",
        ].some((path) => pathname === path || pathname.startsWith(path)) && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Export data"
              // onClick={() => handleOpenModal('export')}
            >
              Export
            </Button>
          </>
        )}

        {/* settings page - Search input and Export */}
        {pathname === "/settings/accounts" && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Add System User"
              // onClick={() => handleOpenModal('export')}
            >
              Add System User
            </Button>
          </>
        )}

        {/* roles page - Search input and Export */}
        {pathname === "/settings/roles" && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Add Role"
              // onClick={() => handleOpenModal('export')}
            >
              Add Role
            </Button>
          </>
        )}

        {/* divisions page - Search input and Export */}
        {pathname === "/settings/divisions" && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Add Division"
              // onClick={() => handleOpenModal('export')}
            >
              Add Division
            </Button>
          </>
        )}

        {/* types page - Search input and Export */}
        {pathname === "/settings/types" && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Add Type"
              // onClick={() => handleOpenModal('export')}
            >
              Add Type
            </Button>
          </>
        )}

        {/* categories page - Search input and Export */}
        {pathname === "/settings/categories" && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Add Category"
              // onClick={() => handleOpenModal('export')}
            >
              Add Category
            </Button>
          </>
        )}

        {/* goal preferences page - Search input and Export */}
        {pathname === "/settings/goal-preferences" && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Add Goal Preference"
              // onClick={() => handleOpenModal('export')}
            >
              Add Goal Preference
            </Button>
          </>
        )}

        {/* Tags page - Search input and Export */}
        {pathname === "/settings/tags" && (
          <>
            <Search />
            <Button icon={<AdjustIcon />} color="default" variant="solid" />

            <SortTable />
            <Button
              type="primary"
              icon={<PlusIcon />}
              aria-label="Add Tag"
              // onClick={() => handleOpenModal('export')}
            >
              Add Tag
            </Button>
          </>
        )}
      </Space>

      {/* Dynamic modal for different actions */}
      <DynamicModal
        visible={modalVisible}
        onCancel={handleCloseModal}
        width={"770px"}
        className="action-modal"
        title={
          modalType === "add"
            ? "Add new article"
            : modalType === "export"
            ? "Export articles"
            : modalType === "upload"
            ? "Upload media"
            : "Modal"
        }
        children={
          modalType === "add" ? (
            <ArticleFormContent />
          ) : modalType === "export" ? (
            <ExportFormContent />
          ) : modalType === "upload" ? (
            <ExportFormContent />
          ) : null
        }
        footerButtons={
          modalType === "add"
            ? [
                <Button
                  key="cancel"
                  onClick={handleCloseModal}
                  className="atn-btn btn-lg"
                >
                  Cancel
                </Button>,
                <Button
                  key="draft"
                  type="default"
                  color="primary"
                  variant="outlined"
                  className="atn-btn btn-lg"
                >
                  {" "}
                  Save as Draft{" "}
                </Button>,
                <Button key="submit" type="primary" className="atn-btn btn-lg">
                  {" "}
                  Continue{" "}
                </Button>,
              ]
            : [
                <Button key="cancel" onClick={handleCloseModal}>
                  Cancel
                </Button>,
                <Button key="submit" type="primary">
                  {modalType === "export"
                    ? "Export"
                    : modalType === "upload"
                    ? "Upload"
                    : "Submit"}
                </Button>,
              ]
        }
      />
    </AntHeader>
  );
};

export default Header;
