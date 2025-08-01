# Contributing to Grow Healthy

Welcome to the Grow Healthy project! This document provides guidelines and best practices for contributing to this Frappe-based application that uses React SDK for frontend development.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Development Setup](#development-setup)
3. [Code Style Guidelines](#code-style-guidelines)
4. [Frappe Development Guidelines](#frappe-development-guidelines)
5. [React SDK Guidelines](#react-sdk-guidelines)
6. [API Development Guidelines](#api-development-guidelines)
7. [Testing Guidelines](#testing-guidelines)
8. [Documentation Guidelines](#documentation-guidelines)
9. [Workflow and Git Guidelines](#workflow-and-git-guidelines)
10. [Security Guidelines](#security-guidelines)
11. [Performance Guidelines](#performance-guidelines)
12. [Frappe Coding Standards](#frappe-coding-standards)

## Project Overview

Grow Healthy is a Frappe-based application that provides React views for Frappe doctypes without the need for custom code. The project combines:

- **Backend**: Frappe Framework (Python)
- **Frontend**: React SDK for Frappe
- **Database**: MySQL/MariaDB
- **Architecture**: RESTful APIs with React components

### Key Components

- **Doctypes**: Custom document types for workflow management
- **APIs**: RESTful endpoints for frontend communication
- **React Components**: Frontend components for user interface
- **Workflows**: Status-based document management system
- **Templates**: HTML templates for custom pages

## Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL/MariaDB
- Frappe Framework 15+

### Installation

1. **Install Frappe dependencies**

   ```bash
   bench get-app <repository-url>
   bench install-app g_healthy
   bench --site <sitename> migrate
   ```

2. **Setup development environment**
   ```bash
   bench start
   ```

### Development Commands

```bash
# Start development server
bench start

# Run tests
bench run-tests g_healthy

# Build assets
bench build

# Migrate database
bench migrate
```

## Code Style Guidelines

### Python Code Style

Follow **PEP 8** standards with Frappe-specific conventions:

```python
# Good
import frappe
from frappe.model.document import Document

class CustomDocument(Document):
    """Custom document class with proper docstring."""

    def validate(self):
        """Validate document before save."""
        super().validate()
        self._validate_custom_fields()

    def _validate_custom_fields(self):
        """Private method for custom validation."""
        if not self.field_name:
            frappe.throw("Field name is required")
```

### JavaScript/React Code Style

Follow **ESLint** and **Prettier** standards:

```javascript
// Good
import React, { useState, useEffect } from "react";
import { useFrappeGetCall } from "frappe-react-sdk";

const CustomComponent = ({ docName }) => {
  const [data, setData] = useState(null);

  const { data: docData, loading } = useFrappeGetCall(
    "g_healthy.api.get_document",
    { doc_name: docName }
  );

  useEffect(() => {
    if (docData) {
      setData(docData);
    }
  }, [docData]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="custom-component">
      <h3>{data?.title}</h3>
    </div>
  );
};

export default CustomComponent;
```

### File Naming Conventions

- **Python files**: `snake_case.py`
- **JavaScript files**: `camelCase.js` or `PascalCase.jsx`
- **JSON files**: `snake_case.json`
- **CSS/SCSS files**: `kebab-case.css`

## Frappe Development Guidelines

### Doctype Development

1. **Create doctypes using Frappe Desk**

   - Use the DocType builder for standard doctypes
   - Create JSON files manually for complex doctypes
   - Customize the default doctypes using customize form
   - Export the customization in a specific module

2. **Field Naming**

   ```python
   # Use descriptive field names
   fieldname = "project_concept_name"  # Good
   fieldname = "name"                  # Avoid generic names
   ```

3. **Permissions**

   ```json
   {
     "permissions": [
       {
         "role": "Grow Healthy User",
         "read": 1,
         "write": 1,
         "create": 1,
         "delete": 0
       }
     ]
   }
   ```

4. **Custom Methods**

   ```python
   class CustomDocType(Document):
       def validate(self):
           super().validate()
           self._validate_workflow_status()

       def _validate_workflow_status(self):
           """Validate workflow status transitions."""
           if self.status == "Finalized" and self.has_permission("write"):
               frappe.throw("Cannot modify finalized documents")
   ```

## API Development Guidelines

### Standard Frappe API Response Format

All APIs should follow this consistent response format:

```python
def standard_response(data=None, error=None, message=None, status_code=200):
    """
    Standard API response format for all endpoints.

    Args:
        data: Response data
        error: Error message if any
        message: Success/info message
        status_code: HTTP status code

    Returns:
        dict: Standardized response
    """
    response = {
        "success": error is None,
        "data": data,
        "message": message,
        "status_code": status_code
    }

    if error:
        response["error"] = str(error)
        response["success"] = False

    return response
```

### RESTful API Structure

1. **Document CRUD Operations**

   ```python
   # In apis/document_api.py
   import frappe
   from frappe import _

   @frappe.whitelist()
   def create_document(doctype, data):
       """Create a new document."""
       try:
           # Validate input
           if not doctype or not data:
               return standard_response(
                   error="Doctype and data are required",
                   status_code=400
               )

           # Check permissions
           if not frappe.has_permission(doctype, "create"):
               return standard_response(
                   error="Permission denied",
                   status_code=403
               )

           # Create document
           doc = frappe.get_doc({
               "doctype": doctype,
               **data
           })
           doc.insert()

           return standard_response(
               data=doc.as_dict(),
               message="Document created successfully",
               status_code=201
           )

       except Exception as e:
           frappe.log_error(f"Error creating document: {str(e)}")
           return standard_response(
               error="Failed to create document",
               status_code=500
           )

   @frappe.whitelist()
   def get_document(doctype, doc_name):
       """Get a single document."""
       try:
           if not frappe.has_permission(doctype, "read", doc_name):
               return standard_response(
                   error="Permission denied",
                   status_code=403
               )

           doc = frappe.get_doc(doctype, doc_name)
           return standard_response(
               data=doc.as_dict(),
               message="Document retrieved successfully"
           )

       except frappe.DoesNotExistError:
           return standard_response(
               error="Document not found",
               status_code=404
           )
       except Exception as e:
           frappe.log_error(f"Error retrieving document: {str(e)}")
           return standard_response(
               error="Failed to retrieve document",
               status_code=500
           )

   @frappe.whitelist()
   def update_document(doctype, doc_name, data):
       """Update an existing document."""
       try:
           if not frappe.has_permission(doctype, "write", doc_name):
               return standard_response(
                   error="Permission denied",
                   status_code=403
               )

           doc = frappe.get_doc(doctype, doc_name)
           doc.update(data)
           doc.save()

           return standard_response(
               data=doc.as_dict(),
               message="Document updated successfully"
           )

       except Exception as e:
           frappe.log_error(f"Error updating document: {str(e)}")
           return standard_response(
               error="Failed to update document",
               status_code=500
           )

   @frappe.whitelist()
   def delete_document(doctype, doc_name):
       """Delete a document."""
       try:
           if not frappe.has_permission(doctype, "delete", doc_name):
               return standard_response(
                   error="Permission denied",
                   status_code=403
               )

           frappe.delete_doc(doctype, doc_name)

           return standard_response(
               message="Document deleted successfully"
           )

       except Exception as e:
           frappe.log_error(f"Error deleting document: {str(e)}")
           return standard_response(
               error="Failed to delete document",
               status_code=500
           )
   ```

2. **List Operations with Pagination**

   ```python
   @frappe.whitelist()
   def get_document_list(doctype, filters=None, fields=None,
                        page=1, limit=20, order_by="creation desc"):
       """Get paginated list of documents."""
       try:
           # Validate permissions
           if not frappe.has_permission(doctype, "read"):
               return standard_response(
                   error="Permission denied",
                   status_code=403
               )

           # Calculate pagination
           start = (page - 1) * limit

           # Get documents
           docs = frappe.get_list(
               doctype,
               filters=filters or {},
               fields=fields or ["name", "creation", "modified"],
               start=start,
               limit=limit,
               order_by=order_by
           )

           # Get total count
           total = frappe.db.count(doctype, filters=filters or {})

           return standard_response(
               data={
                   "documents": docs,
                   "pagination": {
                       "page": page,
                       "limit": limit,
                       "total": total,
                       "pages": (total + limit - 1) // limit,
                       "has_next": (page * limit) < total,
                       "has_prev": page > 1
                   }
               },
               message="Documents retrieved successfully"
           )

       except Exception as e:
           frappe.log_error(f"Error retrieving document list: {str(e)}")
           return standard_response(
               error="Failed to retrieve documents",
               status_code=500
           )
   ```

3. **Search and Filter Operations**

   ```python
   @frappe.whitelist()
   def search_documents(doctype, search_term, filters=None,
                       fields=None, limit=20):
       """Search documents by term."""
       try:
           if not frappe.has_permission(doctype, "read"):
               return standard_response(
                   error="Permission denied",
                   status_code=403
               )

           # Build search filters
           search_filters = filters or {}
           search_filters["name"] = ["like", f"%{search_term}%"]

           docs = frappe.get_list(
               doctype,
               filters=search_filters,
               fields=fields or ["name", "title", "status"],
               limit=limit,
               order_by="creation desc"
           )

           return standard_response(
               data=docs,
               message=f"Found {len(docs)} documents"
           )

       except Exception as e:
           frappe.log_error(f"Error searching documents: {str(e)}")
           return standard_response(
               error="Failed to search documents",
               status_code=500
           )
   ```

### Error Handling

```python
def handle_api_errors(func):
    """Decorator for consistent error handling in APIs."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except frappe.PermissionError:
            return standard_response(
                error="Permission denied",
                status_code=403
            )
        except frappe.DoesNotExistError:
            return standard_response(
                error="Resource not found",
                status_code=404
            )
        except frappe.ValidationError as e:
            return standard_response(
                error=str(e),
                status_code=400
            )
        except Exception as e:
            frappe.log_error(f"API Error in {func.__name__}: {str(e)}")
            return standard_response(
                error="Internal server error",
                status_code=500
            )
    return wrapper
```

### Rate Limiting

```python
from functools import wraps
import time

def rate_limit(max_requests=100, window=3600):
    """Rate limiting decorator for APIs."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = frappe.session.user
            cache_key = f"rate_limit:{user}:{func.__name__}"

            # Check rate limit
            current_requests = frappe.cache().get_value(cache_key) or 0

            if current_requests >= max_requests:
                return standard_response(
                    error="Rate limit exceeded",
                    status_code=429
                )

            # Increment counter
            frappe.cache().set_value(cache_key, current_requests + 1,
                                   expires_in_sec=window)

            return func(*args, **kwargs)
        return wrapper
    return decorator
```

## React SDK Guidelines

### Component Structure

1. **Functional Components with Hooks**

   ```javascript
   import React, { useState, useEffect } from "react";
   import { useFrappeGetCall, useFrappeUpdateCall } from "frappe-react-sdk";

   const DocumentForm = ({ docName }) => {
     const [formData, setFormData] = useState({});
     const [errors, setErrors] = useState({});

     const { data, loading, error } = useFrappeGetCall(
       "g_healthy.api.get_document",
       { doc_name: docName }
     );

     const { call: updateDoc } = useFrappeUpdateCall();

     const handleSubmit = async (formData) => {
       try {
         const result = await updateDoc({
           doctype: "Custom DocType",
           name: docName,
           data: formData,
         });

         if (result.success) {
           // Handle success
           console.log(result.message);
         } else {
           // Handle error
           setErrors(result.error);
         }
       } catch (error) {
         setErrors({ general: "Failed to update document" });
       }
     };

     if (loading) return <div>Loading...</div>;
     if (error) return <div>Error: {error}</div>;

     return <div className="document-form">{/* Form JSX */}</div>;
   };
   ```

2. **Custom Hooks for API Calls**

   ```javascript
   // hooks/useDocument.js
   import { useFrappeGetCall } from "frappe-react-sdk";

   export const useDocument = (doctype, docName) => {
     const { data, loading, error } = useFrappeGetCall(
       "g_healthy.api.get_document",
       { doctype, doc_name: docName }
     );

     return {
       data: data?.data,
       loading,
       error: error || data?.error,
     };
   };

   // hooks/useDocumentList.js
   export const useDocumentList = (doctype, filters, page = 1, limit = 20) => {
     const { data, loading, error } = useFrappeGetCall(
       "g_healthy.api.get_document_list",
       { doctype, filters, page, limit }
     );

     return {
       documents: data?.data?.documents || [],
       pagination: data?.data?.pagination || {},
       loading,
       error: error || data?.error,
     };
   };
   ```

### State Management

1. **Local State**

   ```javascript
   const [localState, setLocalState] = useState({
     formData: {},
     errors: {},
     loading: false,
     success: false,
   });
   ```

2. **Context for Global State**

   ```javascript
   // contexts/AppContext.js
   import React, { createContext, useContext, useReducer } from "react";

   const AppContext = createContext();

   const initialState = {
     user: null,
     permissions: {},
     notifications: [],
   };

   const appReducer = (state, action) => {
     switch (action.type) {
       case "SET_USER":
         return { ...state, user: action.payload };
       case "SET_PERMISSIONS":
         return { ...state, permissions: action.payload };
       case "ADD_NOTIFICATION":
         return {
           ...state,
           notifications: [...state.notifications, action.payload],
         };
       default:
         return state;
     }
   };

   export const AppProvider = ({ children }) => {
     const [state, dispatch] = useReducer(appReducer, initialState);

     return (
       <AppContext.Provider value={{ state, dispatch }}>
         {children}
       </AppContext.Provider>
     );
   };

   export const useAppContext = () => {
     const context = useContext(AppContext);
     if (!context) {
       throw new Error("useAppContext must be used within AppProvider");
     }
     return context;
   };
   ```

### Form Handling

1. **Controlled Components**

   ```javascript
   const FormField = ({ label, value, onChange, error, type = "text" }) => (
     <div className="form-group">
       <label>{label}</label>
       <input
         type={type}
         value={value || ""}
         onChange={(e) => onChange(e.target.value)}
         className={error ? "error" : ""}
       />
       {error && <span className="error-text">{error}</span>}
     </div>
   );
   ```

2. **Form Validation**

   ```javascript
   const validateForm = (data, rules) => {
     const errors = {};

     Object.keys(rules).forEach((field) => {
       const value = data[field];
       const rule = rules[field];

       if (rule.required && !value) {
         errors[field] = `${field} is required`;
       } else if (rule.pattern && !rule.pattern.test(value)) {
         errors[field] = rule.message || `${field} is invalid`;
       }
     });

     return errors;
   };
   ```

## Testing Guidelines

### Python Testing

1. **Unit Tests**

   ```python
   # test_custom_doctype.py
   import frappe
   from frappe.tests.utils import FrappeTestCase

   class TestCustomDocType(FrappeTestCase):
       def setUp(self):
           """Set up test data."""
           self.doc = frappe.get_doc({
               "doctype": "Custom DocType",
               "title": "Test Document"
           })

       def test_validation(self):
           """Test document validation."""
           self.doc.insert()
           self.assertTrue(self.doc.name)

       def test_workflow_status(self):
           """Test workflow status transitions."""
           self.doc.status = "Finalized"
           self.doc.save()
           self.assertEqual(self.doc.status, "Finalized")
   ```

2. **API Tests**

   ```python
   class TestAPIEndpoints(FrappeTestCase):
       def test_get_document_api(self):
           """Test document retrieval API."""
           # Create test document
           doc = frappe.get_doc({
               "doctype": "Custom DocType",
               "title": "Test API"
           }).insert()

           # Test API call
           result = frappe.call("g_healthy.api.get_document", {
               "doctype": "Custom DocType",
               "doc_name": doc.name
           })

           self.assertTrue(result.get("success"))
           self.assertEqual(result["data"]["title"], "Test API")
   ```

### React Testing

1. **Component Tests**

   ```javascript
   // __tests__/CustomComponent.test.js
   import React from "react";
   import { render, screen } from "@testing-library/react";
   import CustomComponent from "../CustomComponent";

   describe("CustomComponent", () => {
     it("renders correctly", () => {
       render(<CustomComponent docName="test-doc" />);
       expect(screen.getByText("Loading...")).toBeInTheDocument();
     });

     it("displays data when loaded", async () => {
       render(<CustomComponent docName="test-doc" />);
       // Add async test logic
     });
   });
   ```

## Documentation Guidelines

### Code Documentation

1. **Python Docstrings**

   ```python
   def process_workflow_document(doc_name, new_status):
       """
       Process workflow document status change.

       Args:
           doc_name (str): Name of the document
           new_status (str): New status to set

       Returns:
           dict: Processing result with standard response format

       Raises:
           frappe.ValidationError: If status transition is invalid
       """
       pass
   ```

2. **JavaScript Comments**
   ```javascript
   /**
    * Custom hook for document management
    * @param {string} doctype - Document type
    * @param {string} docName - Document name
    * @returns {Object} Document data and loading state
    */
   const useDocument = (doctype, docName) => {
     // Implementation
   };
   ```

### README Files

Create README files for each major component:

````markdown
# Component Name

Brief description of the component.

## Usage

```javascript
import ComponentName from "./ComponentName";

<ComponentName prop1="value" prop2="value" />;
```
````

## Props

| Prop  | Type   | Required | Description |
| ----- | ------ | -------- | ----------- |
| prop1 | string | Yes      | Description |
| prop2 | number | No       | Description |

## Examples

[Code examples]

## API Reference

[API documentation]

```

## Workflow and Git Guidelines

### Branch Naming

- `feature/component-name` - New features
- `bugfix/issue-description` - Bug fixes
- `hotfix/critical-fix` - Critical fixes
- `docs/documentation-update` - Documentation updates

### Commit Messages

Follow conventional commit format:

```

type(scope): description

[optional body]

[optional footer]

```

Examples:
```

feat(api): add document creation endpoint
fix(ui): resolve form validation error
docs(readme): update installation instructions

````

### Pull Request Process

1. **Create feature branch**
2. **Write tests** for new functionality
3. **Update documentation**
4. **Run linting and tests**
5. **Create pull request** with detailed description
6. **Code review** by team members
7. **Merge** after approval

## Security Guidelines

### Input Validation

1. **Server-side validation**
   ```python
   def validate_user_input(data):
       """Validate all user inputs."""
       if not isinstance(data, dict):
           frappe.throw("Invalid data format")

       required_fields = ["title", "description"]
       for field in required_fields:
           if field not in data or not data[field]:
               frappe.throw(f"Field {field} is required")
````

2. **SQL Injection Prevention**

   ```python
   # Good - Use Frappe's ORM
   docs = frappe.get_list("Custom DocType", filters={"status": status})

   # Bad - Direct SQL (avoid)
   docs = frappe.db.sql("SELECT * FROM tabCustom DocType WHERE status = %s", status)
   ```

### Authentication and Authorization

1. **Permission Checks**

   ```python
   @frappe.whitelist()
   def secure_api_call(doctype, doc_name):
       """Secure API with permission checks."""
       if not frappe.has_permission(doctype, "read", doc_name):
           return standard_response(
               error="Permission denied",
               status_code=403
           )

       return standard_response(
           data=frappe.get_doc(doctype, doc_name).as_dict()
       )
   ```

2. **Role-based Access**
   ```python
   def check_user_role(allowed_roles):
       """Check if user has required role."""
       user_roles = frappe.get_roles(frappe.session.user)
       return any(role in user_roles for role in allowed_roles)
   ```

## Performance Guidelines

### Database Optimization

1. **Indexing**

   ```python
   # Add indexes for frequently queried fields
   # In doctype JSON file
   {
       "fields": [
           {
               "fieldname": "status",
               "fieldtype": "Select",
               "index": 1  # Add index
           }
       ]
   }
   ```

2. **Query Optimization**

   ```python
   # Good - Select only needed fields
   docs = frappe.get_list("Custom DocType",
                          fields=["name", "title", "status"],
                          filters={"status": "Active"})

   # Bad - Select all fields
   docs = frappe.get_list("Custom DocType",
                          filters={"status": "Active"})
   ```

### Frontend Performance

1. **Component Optimization**

   ```javascript
   // Use React.memo for expensive components
   const ExpensiveComponent = React.memo(({ data }) => {
     return <div>{/* Expensive rendering */}</div>;
   });

   // Use useMemo for expensive calculations
   const expensiveValue = useMemo(() => {
     return computeExpensiveValue(data);
   }, [data]);
   ```

2. **API Call Optimization**
   ```javascript
   // Use caching for repeated API calls
   const { data } = useFrappeGetCall(
     "g_healthy.api.get_document",
     { doc_name: docName },
     { cache: true, cacheTime: 5 * 60 * 1000 } // 5 minutes
   );
   ```

## Frappe Coding Standards

Following the [Frappe Coding Standards](https://github.com/frappe/erpnext/wiki/Coding-Standards), here are the key guidelines:

### 1. **Python Code Style**

- **Indentation**: Use 4 spaces, never tabs
- **Line Length**: Maximum 120 characters
- **Import Order**: Standard library → Third-party → Local imports
- **Naming**: Use snake_case for functions and variables

```python
# Good - Proper import order
import os
import sys
from datetime import datetime

import frappe
from frappe import _

from g_healthy.utils import helper_function

# Good - Proper naming
def get_user_data(user_id):
    """Get user data from database."""
    return frappe.get_doc("User", user_id)

# Bad - Wrong naming
def GetUserData(userId):
    return frappe.get_doc("User", userId)
```

### 2. **DocType Development**

- **Field Names**: Use descriptive, lowercase names
- **Validation**: Always validate in the `validate()` method
- **Permissions**: Define clear permission rules

```python
# Good - Proper DocType structure
class CustomDocType(Document):
    def validate(self):
        super().validate()
        self._validate_required_fields()
        self._validate_business_logic()

    def _validate_required_fields(self):
        """Validate required fields."""
        if not self.title:
            frappe.throw(_("Title is required"))

    def _validate_business_logic(self):
        """Validate business logic."""
        if self.status == "Finalized" and self.has_permission("write"):
            frappe.throw(_("Cannot modify finalized documents"))
```

### 3. **API Development**

- **Whitelist**: Always use `@frappe.whitelist()` for public APIs
- **Error Handling**: Use proper exception handling
- **Logging**: Log errors appropriately

```python
@frappe.whitelist()
def create_document(doctype, data):
    """Create a new document with proper error handling."""
    try:
        if not frappe.has_permission(doctype, "create"):
            frappe.throw(_("Permission denied"))

        doc = frappe.get_doc({
            "doctype": doctype,
            **data
        })
        doc.insert()

        return {
            "success": True,
            "data": doc.as_dict(),
            "message": _("Document created successfully")
        }
    except Exception as e:
        frappe.log_error(f"Error creating document: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
```

### 4. **JavaScript/React Standards**

- **Component Naming**: Use PascalCase for components
- **Props**: Use camelCase for prop names
- **State**: Use descriptive state variable names

```javascript
// Good - Proper React component structure
import React, { useState, useEffect } from "react";
import { useFrappeGetCall } from "frappe-react-sdk";

const DocumentForm = ({ docName, onSave }) => {
  const [formData, setFormData] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const { data, loading, error } = useFrappeGetCall(
    "g_healthy.api.get_document",
    { doc_name: docName }
  );

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);

    try {
      // Handle form submission
      await onSave(formData);
    } catch (error) {
      console.error("Form submission error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return <form onSubmit={handleSubmit}>{/* Form content */}</form>;
};

export default DocumentForm;
```

### 5. **Database Standards**

- **Queries**: Use Frappe's ORM methods
- **Indexing**: Add indexes for frequently queried fields
- **Performance**: Optimize queries for large datasets

```python
# Good - Use Frappe ORM
docs = frappe.get_list(
    "Custom DocType",
    filters={"status": "Active"},
    fields=["name", "title", "creation"],
    order_by="creation desc",
    limit=20
)

# Bad - Direct SQL (avoid)
docs = frappe.db.sql("""
    SELECT name, title, creation
    FROM `tabCustom DocType`
    WHERE status = 'Active'
    ORDER BY creation DESC
    LIMIT 20
""", as_dict=True)
```

### 6. **Frappe v15 Migration Considerations**

Based on the [Frappe v15 migration guide](https://github.com/frappe/frappe/wiki/Migrating-to-version-15), ensure your code follows these standards:

- **Database Methods**: Use updated Frappe database methods
- **Vue 3 Migration**: If using Vue components, migrate to Vue 3
- **Server Scripts**: Be aware of server script restrictions
- **Timezone Utils**: Use updated timezone utility functions

```python
# Updated database methods for v15
# Good - Use db.set_single_value for single doctypes
frappe.db.set_single_value("System Settings", "timezone", "UTC")

# Bad - Old method (removed in v15)
# frappe.db.set_value("System Settings", None, "timezone", "UTC")

# Updated timezone imports
from frappe.utils.data import convert_utc_to_system_timezone, get_system_timezone

# Updated compare function
from frappe.utils import compare
compare(val1, operator, val2)
```

## Conclusion

Following these guidelines will ensure:

- **Consistent code quality** across the project
- **Maintainable and scalable** codebase
- **Secure and performant** application
- **Better collaboration** among team members
- **Easier onboarding** for new contributors

Remember to:

- Always write tests for new functionality
- Update documentation when making changes
- Follow the established patterns in the codebase
- Ask for help when unsure about implementation details

Happy coding! 🚀
