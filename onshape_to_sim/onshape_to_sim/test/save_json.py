import argparse
import json

json_string = """
{
  "prev": null,
  "next": null,
  "href": "https://cad.onshape.com/api/metadata/d/6041e7103bb40af449a81618/v/ed106544befb4ae92eea036d/e/7a12328807be40cb1472cc52/p?configuration=default",
  "items": [
    {
      "jsonType": "metadata-part",
      "isMesh": false,
      "partId": "JHD",
      "isFlattenedBody": false,
      "partType": "solid",
      "meshState": 0,
      "properties": [
        {
          "name": "Appearance",
          "value": {
            "color": {
              "red": 204,
              "green": 204,
              "blue": 204
            },
            "isGenerated": false,
            "opacity": 255
          },
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 3,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d60c",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "OBJECT",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Name",
          "value": "Body",
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 3,
          "validator": {
            "min": null,
            "max": null,
            "minLength": 1,
            "maxLength": 256,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": true,
          "propertyId": "57f3fb8efa3416c06701d60d",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce0",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Description",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d60e",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce0",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": true
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Category",
          "value": [
            {
              "memberCategoryIds": null,
              "memberCategories": null,
              "description": "Category created by upgrade",
              "ownerType": 2,
              "ownerId": "556f3109e4b00b3fee9a3f4a",
              "publishState": 1,
              "objectTypes": [
                2
              ],
              "defaultObjectType": 2,
              "name": "Onshape Part",
              "id": "5877a03ebe4c21163b49dce2",
              "href": null
            }
          ],
          "defaultValue": [
            {
              "memberCategoryIds": null,
              "memberCategories": null,
              "description": "Category created by upgrade",
              "ownerType": 2,
              "ownerId": "556f3109e4b00b3fee9a3f4a",
              "publishState": 1,
              "objectTypes": [
                2
              ],
              "defaultObjectType": 2,
              "name": "Onshape Part",
              "id": "5877a03ebe4c21163b49dce2",
              "href": null
            }
          ],
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d625",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "CATEGORY",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce0",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Part number",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 128,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d60f",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Revision",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d610",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "State",
          "value": "0",
          "defaultValue": "0",
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": null,
          "required": true,
          "propertyId": "57f3fb8efa3416c06701d611",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "ENUM",
          "enumValues": [
            {
              "value": "0",
              "state": 0,
              "label": "In progress"
            },
            {
              "value": "1",
              "state": 0,
              "label": "Pending"
            },
            {
              "value": "2",
              "state": 0,
              "label": "Released"
            },
            {
              "value": "3",
              "state": 0,
              "label": "Obsolete"
            },
            {
              "value": "4",
              "state": 0,
              "label": "Rejected"
            },
            {
              "value": "5",
              "state": 0,
              "label": "Discarded"
            }
          ],
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Vendor",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d612",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Project",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d613",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Product line",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d614",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Material",
          "value": {
            "properties": [
              {
                "name": "DENS",
                "value": "8030",
                "type": "REAL",
                "displayName": "Density",
                "units": "kg/m^3",
                "category": "Physical",
                "description": "Density"
              }
            ],
            "id": "A2 Stainless Steel",
            "displayName": "A2 Stainless Steel",
            "libraryName": "Onshape Material Library",
            "libraryReference": {
              "versionId": "e0c061103dc54e43d0f4f92c",
              "documentId": "2718281828459eacfeeda11f",
              "elementId": "6bbab304a1f64e7d640a2d7d",
              "elementMicroversionId": "3ddb8491f577da0c2d4166ea"
            }
          },
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 3,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d615",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "OBJECT",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Title 1",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d616",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Title 2",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d617",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Title 3",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d618",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Not revision managed",
          "value": false,
          "defaultValue": false,
          "computedPropertyError": null,
          "propertySource": 6,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d61d",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "BOOL",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Exclude from BOM",
          "value": false,
          "defaultValue": false,
          "computedPropertyError": null,
          "propertySource": 6,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d61e",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "BOOL",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Unit of measure",
          "value": "Each",
          "defaultValue": "Each",
          "computedPropertyError": null,
          "propertySource": 6,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d623",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "ENUM",
          "enumValues": [
            {
              "value": "Centimeter",
              "state": 0,
              "label": null
            },
            {
              "value": "Foot",
              "state": 0,
              "label": null
            },
            {
              "value": "Inch",
              "state": 0,
              "label": null
            },
            {
              "value": "Meter",
              "state": 0,
              "label": null
            },
            {
              "value": "Millimeter",
              "state": 0,
              "label": null
            },
            {
              "value": "Yard",
              "state": 0,
              "label": null
            },
            {
              "value": "Gram",
              "state": 0,
              "label": null
            },
            {
              "value": "Kilogram",
              "state": 0,
              "label": null
            },
            {
              "value": "Ounce",
              "state": 0,
              "label": null
            },
            {
              "value": "Pound",
              "state": 0,
              "label": null
            },
            {
              "value": "Liter",
              "state": 0,
              "label": null
            },
            {
              "value": "Gallon",
              "state": 0,
              "label": null
            },
            {
              "value": "Each",
              "state": 0,
              "label": null
            },
            {
              "value": "Fluid ounce",
              "state": 0,
              "label": null
            },
            {
              "value": "Milliliter",
              "state": 0,
              "label": null
            },
            {
              "value": "Centiliter",
              "state": 0,
              "label": null
            },
            {
              "value": "Package",
              "state": 0,
              "label": null
            }
          ],
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Mass",
          "value": {
            "formattedValue": "2.239 kg",
            "computed": 2.238744814460115,
            "useOverride": false
          },
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 7,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": null,
            "pattern": null,
            "quantityType": 5,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d626",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "COMPUTED",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": true,
          "uiHints": null,
          "propertyOverrideStatus": 2
        },
        {
          "name": "Center of mass",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d627",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "COMPUTED",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Inertia",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d628",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "COMPUTED",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Tessellation quality",
          "value": "0",
          "defaultValue": "0",
          "computedPropertyError": null,
          "propertySource": 6,
          "validator": null,
          "required": true,
          "propertyId": "5ace8269c046ad612c65a0bb",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "ENUM",
          "enumValues": [
            {
              "value": "0",
              "state": 0,
              "label": "Auto"
            },
            {
              "value": "1",
              "state": 0,
              "label": "Coarse"
            },
            {
              "value": "2",
              "state": 0,
              "label": "Medium"
            },
            {
              "value": "3",
              "state": 0,
              "label": "Fine"
            },
            {
              "value": "4",
              "state": 0,
              "label": "Very fine"
            }
          ],
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        }
      ],
      "href": "https://cad.onshape.com/api/metadata/d/6041e7103bb40af449a81618/v/ed106544befb4ae92eea036d/e/7a12328807be40cb1472cc52/p/JHD?configuration=default"
    },
    {
      "jsonType": "metadata-part",
      "isMesh": false,
      "partId": "JYD",
      "partIdentity": "cdfb271be2a3d06a9bff3193",
      "isFlattenedBody": false,
      "partType": "solid",
      "meshState": 0,
      "properties": [
        {
          "name": "Appearance",
          "value": {
            "color": {
              "red": 67,
              "green": 72,
              "blue": 77
            },
            "isGenerated": false,
            "opacity": 255
          },
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 3,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d60c",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "OBJECT",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Name",
          "value": "Wheel",
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 3,
          "validator": {
            "min": null,
            "max": null,
            "minLength": 1,
            "maxLength": 256,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": true,
          "propertyId": "57f3fb8efa3416c06701d60d",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce0",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Description",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d60e",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce0",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": true
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Category",
          "value": [
            {
              "memberCategoryIds": null,
              "memberCategories": null,
              "description": "Category created by upgrade",
              "ownerType": 2,
              "ownerId": "556f3109e4b00b3fee9a3f4a",
              "publishState": 1,
              "objectTypes": [
                2
              ],
              "defaultObjectType": 2,
              "name": "Onshape Part",
              "id": "5877a03ebe4c21163b49dce2",
              "href": null
            }
          ],
          "defaultValue": [
            {
              "memberCategoryIds": null,
              "memberCategories": null,
              "description": "Category created by upgrade",
              "ownerType": 2,
              "ownerId": "556f3109e4b00b3fee9a3f4a",
              "publishState": 1,
              "objectTypes": [
                2
              ],
              "defaultObjectType": 2,
              "name": "Onshape Part",
              "id": "5877a03ebe4c21163b49dce2",
              "href": null
            }
          ],
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d625",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "CATEGORY",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce0",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Part number",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 128,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d60f",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Revision",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d610",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "State",
          "value": "0",
          "defaultValue": "0",
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": null,
          "required": true,
          "propertyId": "57f3fb8efa3416c06701d611",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "ENUM",
          "enumValues": [
            {
              "value": "0",
              "state": 0,
              "label": "In progress"
            },
            {
              "value": "1",
              "state": 0,
              "label": "Pending"
            },
            {
              "value": "2",
              "state": 0,
              "label": "Released"
            },
            {
              "value": "3",
              "state": 0,
              "label": "Obsolete"
            },
            {
              "value": "4",
              "state": 0,
              "label": "Rejected"
            },
            {
              "value": "5",
              "state": 0,
              "label": "Discarded"
            }
          ],
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Vendor",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d612",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Project",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d613",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Product line",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d614",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Material",
          "value": {
            "properties": [
              {
                "name": "DENS",
                "value": "7740",
                "type": "REAL",
                "displayName": "Density",
                "units": "kg/m^3",
                "category": "Physical",
                "description": "Density"
              }
            ],
            "id": "Stainless Steel",
            "displayName": "Stainless Steel",
            "libraryName": "Onshape Material Library",
            "libraryReference": {
              "versionId": "e0c061103dc54e43d0f4f92c",
              "documentId": "2718281828459eacfeeda11f",
              "elementId": "6bbab304a1f64e7d640a2d7d",
              "elementMicroversionId": "3ddb8491f577da0c2d4166ea"
            }
          },
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 3,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d615",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "OBJECT",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Title 1",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d616",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Title 2",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d617",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Title 3",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": 10000,
            "pattern": null,
            "quantityType": null,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d618",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "STRING",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": {
            "multiline": false
          },
          "propertyOverrideStatus": 0
        },
        {
          "name": "Not revision managed",
          "value": false,
          "defaultValue": false,
          "computedPropertyError": null,
          "propertySource": 6,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d61d",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "BOOL",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Exclude from BOM",
          "value": false,
          "defaultValue": false,
          "computedPropertyError": null,
          "propertySource": 6,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d61e",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "BOOL",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Unit of measure",
          "value": "Each",
          "defaultValue": "Each",
          "computedPropertyError": null,
          "propertySource": 6,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d623",
          "editable": true,
          "editableInUi": true,
          "dateFormat": null,
          "valueType": "ENUM",
          "enumValues": [
            {
              "value": "Centimeter",
              "state": 0,
              "label": null
            },
            {
              "value": "Foot",
              "state": 0,
              "label": null
            },
            {
              "value": "Inch",
              "state": 0,
              "label": null
            },
            {
              "value": "Meter",
              "state": 0,
              "label": null
            },
            {
              "value": "Millimeter",
              "state": 0,
              "label": null
            },
            {
              "value": "Yard",
              "state": 0,
              "label": null
            },
            {
              "value": "Gram",
              "state": 0,
              "label": null
            },
            {
              "value": "Kilogram",
              "state": 0,
              "label": null
            },
            {
              "value": "Ounce",
              "state": 0,
              "label": null
            },
            {
              "value": "Pound",
              "state": 0,
              "label": null
            },
            {
              "value": "Liter",
              "state": 0,
              "label": null
            },
            {
              "value": "Gallon",
              "state": 0,
              "label": null
            },
            {
              "value": "Each",
              "state": 0,
              "label": null
            },
            {
              "value": "Fluid ounce",
              "state": 0,
              "label": null
            },
            {
              "value": "Milliliter",
              "state": 0,
              "label": null
            },
            {
              "value": "Centiliter",
              "state": 0,
              "label": null
            },
            {
              "value": "Package",
              "state": 0,
              "label": null
            }
          ],
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Mass",
          "value": {
            "formattedValue": "0.335 kg",
            "computed": 0.33541920259867763,
            "useOverride": false
          },
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 7,
          "validator": {
            "min": null,
            "max": null,
            "minLength": null,
            "maxLength": null,
            "pattern": null,
            "quantityType": 5,
            "maxCount": null,
            "minCount": null,
            "minDate": null,
            "maxDate": null
          },
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d626",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "COMPUTED",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": true,
          "uiHints": null,
          "propertyOverrideStatus": 2
        },
        {
          "name": "Center of mass",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d627",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "COMPUTED",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Inertia",
          "value": null,
          "defaultValue": null,
          "computedPropertyError": null,
          "propertySource": 0,
          "validator": null,
          "required": false,
          "propertyId": "57f3fb8efa3416c06701d628",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "COMPUTED",
          "enumValues": null,
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        },
        {
          "name": "Tessellation quality",
          "value": "0",
          "defaultValue": "0",
          "computedPropertyError": null,
          "propertySource": 6,
          "validator": null,
          "required": true,
          "propertyId": "5ace8269c046ad612c65a0bb",
          "editable": false,
          "editableInUi": false,
          "dateFormat": null,
          "valueType": "ENUM",
          "enumValues": [
            {
              "value": "0",
              "state": 0,
              "label": "Auto"
            },
            {
              "value": "1",
              "state": 0,
              "label": "Coarse"
            },
            {
              "value": "2",
              "state": 0,
              "label": "Medium"
            },
            {
              "value": "3",
              "state": 0,
              "label": "Fine"
            },
            {
              "value": "4",
              "state": 0,
              "label": "Very fine"
            }
          ],
          "schemaId": "5877a03ebe4c21163b49dce2",
          "multivalued": false,
          "computedAssemblyProperty": false,
          "computedProperty": false,
          "uiHints": null,
          "propertyOverrideStatus": 0
        }
      ],
      "href": "https://cad.onshape.com/api/metadata/d/6041e7103bb40af449a81618/v/ed106544befb4ae92eea036d/e/7a12328807be40cb1472cc52/p/JYD/pi/cdfb271be2a3d06a9bff3193?configuration=default"
    }
  ]
}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    parse_json = json.loads(json_string)
    if not args.filename.endswith(".txt"):
        args.filename = f"{args.filename}.txt"
    data_file = f"data/{args.filename}"
    with open(data_file, "w") as fi:
        json.dump(parse_json, fi)


if __name__ == "__main__":
    main()
