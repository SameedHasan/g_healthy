import frappe
from frappe.core.doctype.doctype.doctype import DocType


class CustomDoctype(DocType):

    def setup_fields_to_fetch(self):
        """Setup query to update values for newly set fetch values"""
        try:
            old_meta = frappe.get_meta(
                frappe.get_doc("DocType", self.name), cached=False
            )
            old_fields_to_fetch = [
                df.fieldname for df in old_meta.get_fields_to_fetch()
            ]
        except frappe.DoesNotExistError:
            old_fields_to_fetch = []

        new_meta = frappe.get_meta(self, cached=False)

        self.flags.update_fields_to_fetch_queries = []

        new_fields_to_fetch = [df for df in new_meta.get_fields_to_fetch()]

        if set(old_fields_to_fetch) != {df.fieldname for df in new_fields_to_fetch}:
            for df in new_fields_to_fetch:
                if df.fieldname not in old_fields_to_fetch:
                    link_fieldname, source_fieldname = df.fetch_from.split(".", 1)
                    if not source_fieldname:
                        continue  # Invalid expression
                    link_df = new_meta.get_field(link_fieldname)

                    if frappe.db.db_type == "postgres":
                        update_query = """
                            UPDATE "tab{doctype}"
                            SET  "{fieldname}" = source."{source_fieldname}"
                            FROM "tab{link_doctype}" AS source
                            WHERE "tab{doctype}"."{link_fieldname}" = source.name
                            AND ("tab{doctype}"."{fieldname}" is null OR "tab{doctype}"."{fieldname}"::text = '') ;
                        """
                    else:
                        update_query = """
							UPDATE `tab{doctype}` as target
							INNER JOIN `tab{link_doctype}` as source
							ON `target`.`{link_fieldname}` = `source`.`name`
							SET `target`.`{fieldname}` = `source`.`{source_fieldname}`
							WHERE ifnull(`target`.`{fieldname}`, '')=""
						"""

                    self.flags.update_fields_to_fetch_queries.append(
                        update_query.format(
                            link_doctype=link_df.options,
                            source_fieldname=source_fieldname,
                            doctype=self.name,
                            fieldname=df.fieldname,
                            link_fieldname=link_fieldname,
                        )
                    )
