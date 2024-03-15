import argparse
import json

json_string = """
{
  "rootAssembly": {
    "occurrences": [
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0.107,
          0,
          1,
          0,
          0,
          0,
          0,
          1,
          -3.469446951953614e-18,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MmRHXBai4kux8tPcZ"
        ]
      },
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0.08927692583203317,
          0,
          1,
          0,
          0.0741149203106761,
          0,
          0,
          1,
          0.06335652424022555,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MrWVPT9IK41t//ORF",
          "MjXp5OEcWIwYLGGrG"
        ]
      },
      {
        "hidden": false,
        "fixed": true,
        "transform": [
          1,
          0,
          0,
          0,
          0,
          1,
          0,
          0,
          0,
          0,
          1,
          0,
          0,
          0,
          0,
          1
        ],
        "path": [
          "ME0OGHafV27m4erd3"
        ]
      },
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0.004736018538475037,
          0,
          1,
          0,
          0.03841717142611742,
          0,
          0,
          1,
          0.09923682259395718,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MrWVPT9IK41t//ORF",
          "MmXPaG80Mq0OnEMRb"
        ]
      },
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0,
          0,
          1,
          0,
          0,
          0,
          0,
          1,
          0,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MfnXxatwJGOcsLj0q"
        ]
      },
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          0.025381017476320267,
          0,
          1,
          0,
          0.06465646903961897,
          0,
          0,
          1,
          0.07801759289577603,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MrWVPT9IK41t//ORF"
        ]
      }
    ],
    "instances": [
      {
        "name": "Body <1>",
        "suppressed": false,
        "id": "ME0OGHafV27m4erd3",
        "type": "Part",
        "isStandardContent": false,
        "partId": "JHD",
        "fullConfiguration": "default",
        "configuration": "default",
        "documentMicroversion": "4a07df152aba423b55fded1f",
        "documentId": "6041e7103bb40af449a81618",
        "elementId": "7a12328807be40cb1472cc52"
      },
      {
        "name": "Wheel <1>",
        "suppressed": false,
        "id": "MfnXxatwJGOcsLj0q",
        "type": "Part",
        "isStandardContent": false,
        "partId": "JYD",
        "fullConfiguration": "default",
        "configuration": "default",
        "documentMicroversion": "4a07df152aba423b55fded1f",
        "documentId": "6041e7103bb40af449a81618",
        "elementId": "7a12328807be40cb1472cc52"
      },
      {
        "name": "Wheel <2>",
        "suppressed": false,
        "id": "MmRHXBai4kux8tPcZ",
        "type": "Part",
        "isStandardContent": false,
        "partId": "JYD",
        "fullConfiguration": "default",
        "configuration": "default",
        "documentMicroversion": "4a07df152aba423b55fded1f",
        "documentId": "6041e7103bb40af449a81618",
        "elementId": "7a12328807be40cb1472cc52"
      },
      {
        "name": "Assembly 1 <1>",
        "suppressed": false,
        "id": "MrWVPT9IK41t//ORF",
        "type": "Assembly",
        "fullConfiguration": "default",
        "configuration": "default",
        "documentMicroversion": "4a07df152aba423b55fded1f",
        "documentId": "6041e7103bb40af449a81618",
        "elementId": "e252e049abc5c4abd6bfe390"
      }
    ],
    "patterns": [],
    "features": [
      {
        "id": "MrDouGkCkF58Czz6o",
        "suppressed": false,
        "featureType": "mate",
        "featureData": {
          "mateType": "REVOLUTE",
          "matedEntities": [
            {
              "matedOccurrence": [
                "MfnXxatwJGOcsLj0q"
              ],
              "matedCS": {
                "xAxis": [
                  0,
                  1,
                  0
                ],
                "yAxis": [
                  0,
                  0,
                  -1
                ],
                "zAxis": [
                  -1,
                  0,
                  0
                ],
                "origin": [
                  -0.02,
                  0.0325,
                  0.024999999999999998
                ]
              }
            },
            {
              "matedOccurrence": [
                "ME0OGHafV27m4erd3"
              ],
              "matedCS": {
                "xAxis": [
                  0,
                  1,
                  0
                ],
                "yAxis": [
                  0,
                  0,
                  -1
                ],
                "zAxis": [
                  -1,
                  0,
                  0
                ],
                "origin": [
                  -0.02,
                  0.0325,
                  0.024999999999999998
                ]
              }
            }
          ],
          "name": "dof_wheel1_speed"
        }
      },
      {
        "id": "M9gO1QTJQd+MmTzeX",
        "suppressed": false,
        "featureType": "mate",
        "featureData": {
          "mateType": "REVOLUTE",
          "matedEntities": [
            {
              "matedOccurrence": [
                "MmRHXBai4kux8tPcZ"
              ],
              "matedCS": {
                "xAxis": [
                  0,
                  1,
                  0
                ],
                "yAxis": [
                  0,
                  0,
                  1
                ],
                "zAxis": [
                  1,
                  0,
                  0
                ],
                "origin": [
                  -0.012,
                  0.032499999999999994,
                  0.024999999999999998
                ]
              }
            },
            {
              "matedOccurrence": [
                "ME0OGHafV27m4erd3"
              ],
              "matedCS": {
                "xAxis": [
                  0,
                  1,
                  0
                ],
                "yAxis": [
                  0,
                  0,
                  1
                ],
                "zAxis": [
                  1,
                  0,
                  0
                ],
                "origin": [
                  0.095,
                  0.0325,
                  0.024999999999999998
                ]
              }
            }
          ],
          "name": "dof_wheel2_speed_inv"
        }
      }
    ],
    "fullConfiguration": "default",
    "configuration": "default",
    "documentMicroversion": "4a07df152aba423b55fded1f",
    "documentId": "6041e7103bb40af449a81618",
    "elementId": "aad7f639435879b7135dce0f"
  },
  "subAssemblies": [
    {
      "instances": [
        {
          "name": "Wheel <1>",
          "suppressed": false,
          "id": "MmXPaG80Mq0OnEMRb",
          "type": "Part",
          "isStandardContent": false,
          "partId": "JYD",
          "fullConfiguration": "default",
          "configuration": "default",
          "documentMicroversion": "4a07df152aba423b55fded1f",
          "documentId": "6041e7103bb40af449a81618",
          "elementId": "7a12328807be40cb1472cc52"
        },
        {
          "name": "Wheel <2>",
          "suppressed": false,
          "id": "MjXp5OEcWIwYLGGrG",
          "type": "Part",
          "isStandardContent": false,
          "partId": "JYD",
          "fullConfiguration": "default",
          "configuration": "default",
          "documentMicroversion": "4a07df152aba423b55fded1f",
          "documentId": "6041e7103bb40af449a81618",
          "elementId": "7a12328807be40cb1472cc52"
        }
      ],
      "patterns": [],
      "features": [],
      "fullConfiguration": "default",
      "configuration": "default",
      "documentMicroversion": "4a07df152aba423b55fded1f",
      "documentId": "6041e7103bb40af449a81618",
      "elementId": "e252e049abc5c4abd6bfe390"
    }
  ],
  "parts": [
    {
      "isStandardContent": false,
      "partId": "JYD",
      "bodyType": "solid",
      "fullConfiguration": "default",
      "configuration": "default",
      "documentMicroversion": "4a07df152aba423b55fded1f",
      "documentId": "6041e7103bb40af449a81618",
      "elementId": "7a12328807be40cb1472cc52"
    },
    {
      "isStandardContent": false,
      "partId": "JHD",
      "bodyType": "solid",
      "fullConfiguration": "default",
      "configuration": "default",
      "documentMicroversion": "4a07df152aba423b55fded1f",
      "documentId": "6041e7103bb40af449a81618",
      "elementId": "7a12328807be40cb1472cc52"
    }
  ],
  "partStudioFeatures": []
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
