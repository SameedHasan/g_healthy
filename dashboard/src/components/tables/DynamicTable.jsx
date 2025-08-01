import React, {
  useState,
  useCallback,
  useMemo,
  useRef,
  useEffect,
} from "react";
import {
  Table,
  Typography,
  Button,
  Tag,
  Row,
  Col,
  Select,
  Pagination,
} from "antd";
import DynamicDrawer from "../drawers/DynamicDrawer";
import DynamicModal from "../modals/DynamicModal";
import ArticleDetailContent from "../content/ArticleDetailContent";
import ArticleFormContent from "../content/ArticleFormContent";
import DeleteConfirmContent from "../content/DeleteConfirmContent";
import "./index.css";
import { useFrappeGetCall, useFrappeGetDoc } from "frappe-react-sdk";

const { Title } = Typography;
const { Option } = Select;

// Reusable function to render status tag
const renderStatusTag = (status) => {
  let color = "green";
  if (status === "Draft") {
    color = "default";
  } else if (status === "Scheduled") {
    color = "orange";
  } else if (status === "Inactive") {
    color = "red";
  }
  return (
    <Tag color={color} key={status}>
      {status}
    </Tag>
  );
};

// Function to open dynamic drawer
export const openDynamicDrawer = (record, type) => {
  const event = new CustomEvent("openDynamicDrawer", {
    detail: { record, type },
  });
  window.dispatchEvent(event);
};

// Function to open dynamic modal
export const openDynamicModal = (record, type) => {
  const event = new CustomEvent("openDynamicModal", {
    detail: { record, type },
  });
  window.dispatchEvent(event);
};

const DynamicTable = ({
  dataType,
  data = [],
  pagination = {},
  searchText = "",
  onSearch,
  onRowClick,
  mediaType = "all",
  page,
}) => {
  // State for UI
  const [loading, setLoading] = useState(false);
  const [pageSize, setPageSize] = useState(10);
  const [sortInfo, setSortInfo] = useState({ field: null, order: null });
  const [drawerVisible, setDrawerVisible] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [actionType, setActionType] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [tableColumns, setTableColumns] = useState([]);
  // const { data:listSettings, error, isLoading, isValidating, mutate } = useFrappeGetDoc("List View Settings", page?.page, page?.page ? `list_view_settings_${page?.page}`: false)
  const {
    data: listSettings,
    error,
    isLoading,
    isValidating,
    mutate,
  } = useFrappeGetCall(
    `g_healthy.v1.system.get_table_columns`,
    {
      doctype: page?.page,
    },
    page?.page ? `list_view_settings_${page?.page}` : false
  );
  const {
    data: dataSource,
    error: dataSoruceError,
    isLoading: dataSrouceLoading,
    isValidating: dataSourceValidating,
    mutate: dataSourceMutate,
  } = useFrappeGetCall("g_healthy.apis.list.get_list", {
    doctype: page?.page,
  });

  // Ref for search input to avoid re-creating debounce function
  const searchInputRef = useRef(null);
  if (error) {
    console.log("error", error);
  }

  // Handle drawer events
  const handleOpenDrawer = useCallback((record, type) => {
    setSelectedRecord(record);
    setActionType(type);
    setDrawerVisible(true);
  }, []);

  const handleCloseDrawer = useCallback(() => {
    setDrawerVisible(false);
  }, []);

  // Handle modal events
  const handleOpenModal = useCallback((record, type) => {
    setSelectedRecord(record);
    setActionType(type);
    setModalVisible(true);
  }, []);

  const handleCloseModal = useCallback(() => {
    setModalVisible(false);
  }, []);

  // Handle table change for sorting
  const handleTableChange = useCallback((pagination, filters, sorter) => {
    if (sorter && sorter.field) {
      setSortInfo({
        field: sorter.field,
        order: sorter.order,
      });
    } else {
      setSortInfo({ field: null, order: null });
    }
  }, []);

  // Handle pagination change
  const handlePaginationChange = useCallback((page) => {
    setCurrentPage(page);
  }, []);

  // Handle page size change
  const handlePageSizeChange = useCallback((size) => {
    setPageSize(size);
    setCurrentPage(1); // Reset to first page when page size changes
  }, []);

  // Add event listeners for dynamic drawer and modal
  useEffect(() => {
    const handleDynamicDrawer = (event) => {
      const { record, type } = event.detail;
      handleOpenDrawer(record, type);
    };

    const handleDynamicModal = (event) => {
      const { record, type } = event.detail;
      handleOpenModal(record, type);
    };

    window.addEventListener("openDynamicDrawer", handleDynamicDrawer);
    window.addEventListener("openDynamicModal", handleDynamicModal);

    return () => {
      window.removeEventListener("openDynamicDrawer", handleDynamicDrawer);
      window.removeEventListener("openDynamicModal", handleDynamicModal);
    };
  }, [handleOpenDrawer, handleOpenModal]);

  // Clean up timeout on unmount
  useEffect(() => {
    return () => {
      if (searchInputRef.current) {
        clearTimeout(searchInputRef.current);
      }
    };
  }, []);

  // Get table columns with sorting capability
  const columns = useMemo(() => {
    if (listSettings?.message && listSettings?.message?.length) {
      // { title: 'ID', dataIndex: 'id', key: 'id', width: 65, fixed: 'left' }
      return listSettings?.message.map((i) => {
        let obj = { ...i };
        if (i.fieldname === "status_field" || i.fieldname === "status") {
          obj.fixed = "right";
          obj.width = "10%";
        }
        return obj;
      });
    } else {
      return [];
    }
  }, [listSettings]);
  useEffect(() => {
    mutate();
  }, [page]);
  // Calculate total items
  const total = 0;

  // Calculate pagination data for current page
  const startIndex = (currentPage - 1) * pageSize;
  const endIndex = startIndex + pageSize;

  // Custom pagination component
  const CustomPagination = () => (
    <Row
      className="custom-pagination"
      justify="space-between"
      align="middle"
      style={{ marginTop: 24 }}
    >
      {/* Left Column: Size Options */}
      <Col>
        <Select value={pageSize} onChange={handlePageSizeChange}>
          {["10", "20", "50", "100"].map((size) => (
            <Option key={size} value={parseInt(size)}>
              {size} / page
            </Option>
          ))}
        </Select>
      </Col>

      {/* Center Column: Pagination */}
      <Col>
        <Pagination
          current={currentPage}
          pageSize={pageSize}
          total={total}
          onChange={handlePaginationChange}
          showSizeChanger={false} // We use custom Select on the left
        />
      </Col>

      {/* Right Column: Total Text */}
      <Col>
        <div className="ant-pagination-total-text">
          {dataType === "Lessons"
            ? `Showing ${(currentPage - 1) * pageSize + 1}-${Math.min(
                currentPage * pageSize,
                total
              )} of ${total} articles`
            : dataType === "media"
            ? `Showing ${(currentPage - 1) * pageSize + 1}-${Math.min(
                currentPage * pageSize,
                total
              )} of ${total} media`
            : `Showing ${(currentPage - 1) * pageSize + 1}-${Math.min(
                currentPage * pageSize,
                total
              )} of ${total} items`}
        </div>
      </Col>
    </Row>
  );

  return (
    <div className="table-ui-container">
      <Table
        columns={columns}
        dataSource={dataSource?.message?.values || []}
        pagination={false} // Disable default pagination
        sticky
        scroll={{ y: "calc(100vh - 290px)" }}
        rowKey="key"
        loading={loading}
        onChange={handleTableChange}
        onRow={
          onRowClick
            ? (record) => ({
                onClick: () => onRowClick(record),
                style: { cursor: "pointer" },
              })
            : undefined
        }
      />

      {/* Custom Pagination */}
      <CustomPagination />

      {/* Dynamic Drawer */}
      <DynamicDrawer
        visible={drawerVisible}
        onClose={handleCloseDrawer}
        title={actionType === "view" ? "Detail" : "Action"}
        extra={null}
        children={
          actionType === "view" && selectedRecord ? (
            <ArticleDetailContent article={selectedRecord} />
          ) : null
        }
      />

      {/* Dynamic Modal */}
      <DynamicModal
        visible={modalVisible}
        onCancel={handleCloseModal}
        className={actionType === "delete" ? "confirmation-modal" : ""}
        width={actionType === "delete" ? "440px" : "770px"}
        title={actionType === "edit" ? "Edit" : ""}
        centered={actionType === "delete" ? true : false}
        children={
          actionType === "edit" ? (
            <ArticleFormContent
              initialData={selectedRecord}
              onChange={() => {}}
            />
          ) : actionType === "delete" ? (
            <DeleteConfirmContent
              item={selectedRecord}
              itemType={dataType === "Lessons" ? "article" : "item"}
            />
          ) : null
        }
        footerButtons={
          actionType === "edit"
            ? [
                <Button
                  className="btn-lg"
                  key="cancel"
                  onClick={handleCloseModal}
                >
                  Cancel
                </Button>,
                <Button className="btn-lg" key="submit" type="primary">
                  Save Changes
                </Button>,
              ]
            : actionType === "delete"
            ? [
                <Button
                  className="btn-lg"
                  key="cancel"
                  onClick={handleCloseModal}
                >
                  Cancel
                </Button>,
                <Button className="btn-lg" key="submit" type="primary">
                  Yes, Delete
                </Button>,
              ]
            : []
        }
      />
    </div>
  );
};

export default DynamicTable;
