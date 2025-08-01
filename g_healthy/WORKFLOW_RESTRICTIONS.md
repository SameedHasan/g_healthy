# Workflow Document Upload Restrictions

This document explains the status-based document upload restrictions implemented in the system to ensure proper workflow compliance.

## Overview

The system now enforces strict document upload restrictions based on the current status of Project Concept I documents. This prevents users from uploading documents out of sequence and ensures the workflow is followed step-by-step.

## Status-Based Restrictions

### Allowed Document Types by Status

| Status                                  | Allowed Documents | Description                                         |
| --------------------------------------- | ----------------- | --------------------------------------------------- |
| New                                     | None              | No documents can be uploaded in New status          |
| Revised                                 | None              | No documents can be uploaded in Revised status      |
| Finalized                               | None              | No documents can be uploaded in Finalized status    |
| Dep Scrutiny                            | None              | No documents can be uploaded in Dep Scrutiny status |
| P&D Scrutiny                            | Working Paper     | Only Working Paper can be uploaded                  |
| Ready For AKDWP                         | MOM               | Only MOM can be uploaded                            |
| Ready For AKCDC                         | MOM               | Only MOM can be uploaded                            |
| MOM Uploaded (Conditionally Approved)   | NOC               | Only NOC can be uploaded                            |
| MOM Uploaded (Unconditionally Approved) | Admin Approval    | Only Admin Approval can be uploaded                 |
| MOM Uploaded (Cleared)                  | MOM               | Only MOM updates allowed                            |
| MOM Uploaded (Deferred)                 | MOM               | Only MOM updates allowed                            |
| NOC Uploaded                            | Admin Approval    | Only Admin Approval can be uploaded                 |
| Admin Approval Uploaded                 | None              | No more documents can be uploaded                   |
| Cancelled                               | None              | No documents can be uploaded in Cancelled status    |

## Document-Specific Requirements

### MOM Document

- Can only be uploaded when status is "Ready For AKDWP", "Ready For AKCDC", "MOM Uploaded (Cleared)", or "MOM Uploaded (Deferred)"
- Requires approval type selection (Conditionally Approved, Unconditionally Approved, Cleared, Deferred)

### NOC Document

- Can only be uploaded after MOM has been uploaded
- Requires MOM approval type to be "Conditionally Approved"

### Admin Approval Document

- Can only be uploaded after MOM has been uploaded
- If MOM approval type is "Conditionally Approved", NOC must also be uploaded
- If MOM approval type is "Unconditionally Approved", can be uploaded directly

## Implementation Details

### File: `g_healthy/overrides/file.py`

The restrictions are implemented in the `CustomFile` class which extends Frappe's default `File` class:

1. **Status Validation**: `_validate_status_based_upload()` checks if the current status allows the document type
2. **Specific Requirements**: `_validate_specific_document_requirements()` enforces document-specific rules
3. **Status Updates**: After successful upload, the document's status is automatically updated

### Key Methods

- `validate()`: Main validation method called during file upload
- `_validate_status_based_upload()`: Checks status-based restrictions
- `_validate_specific_document_requirements()`: Enforces document-specific rules
- `_get_workflow_state_info()`: Helper method for debugging workflow state

## Error Messages

The system provides clear error messages when upload restrictions are violated:

- Status-based errors: "Cannot upload '[Document Type]' document. Current status is '[Status]'. Allowed document types for this status: [List]"
- MOM-specific errors: "Cannot upload MOM document. Current status '[Status]' does not allow MOM uploads."
- NOC-specific errors: "NOC can only be uploaded after MOM has been uploaded."
- Admin Approval errors: "Admin Approval can only be uploaded after MOM has been uploaded."

## Testing

To test the restrictions:

1. Create a Project Concept I document
2. Try uploading documents in different statuses
3. Verify that only allowed document types can be uploaded
4. Check that status updates occur correctly after uploads

## Monitoring

The system logs all upload attempts for monitoring purposes. Check the Frappe logs for entries like:
"File upload attempt: [Document Type] for [DocType] [DocName]"

## Troubleshooting

If uploads are being blocked unexpectedly:

1. Check the current document status
2. Verify the document type is allowed for that status
3. Ensure all prerequisite documents have been uploaded
4. Check the approval type for MOM documents
5. Review the workflow state using the `_get_workflow_state_info()` method
