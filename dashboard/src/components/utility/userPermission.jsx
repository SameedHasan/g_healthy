import { useFrappeGetCall } from 'frappe-react-sdk';
import { useState, useEffect } from 'react';

const usePermission = (doctype) => {
  const [pagePermissions, setPagePermissions] = useState({
    create: 0,
    delete: 0,
    only_owner: 0,
    read: 0,
    update: 0,
  });

  const { data: userPermissions, isLoading: permissionLoading } = useFrappeGetCall("g_healthy.apis.api.check_permissions", {
    doctype
  });

  useEffect(() => {
    if (!permissionLoading && userPermissions?.message) {
      setPagePermissions({
        create: userPermissions.message.create || 0,
        delete: userPermissions.message.delete || 0,
        only_owner: userPermissions.message.only_owner || 0,
        read: userPermissions.message.read || 0,
        update: userPermissions.message.update || 0,
      });
    }
  }, [userPermissions, permissionLoading]);

  return { pagePermissions, permissionLoading };
};

export default usePermission;
