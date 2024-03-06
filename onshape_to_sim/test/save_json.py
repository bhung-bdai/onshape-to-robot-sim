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
          -0.006383226718753576,
          0,
          1,
          0,
          0.008866184777393938,
          0,
          0,
          1,
          -0.0014586132019758224,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MMOby+OjmU+PDKhT8"
        ]
      },
      {
        "hidden": false,
        "fixed": false,
        "transform": [
          1,
          0,
          0,
          -0.08124053478240967,
          0,
          1,
          0,
          -0.08227203677892685,
          0,
          0,
          1,
          -0.07333761674817652,
          0,
          0,
          0,
          1
        ],
        "path": [
          "MvW7NkK9OkQ8TI+lI"
        ]
      }
    ],
    "instances": [
      {
        "name": "Part 1 <1>",
        "suppressed": false,
        "id": "MMOby+OjmU+PDKhT8",
        "type": "Part",
        "isStandardContent": false,
        "partId": "JHD",
        "fullConfiguration": "default",
        "configuration": "default",
        "elementId": "5c9bd028712a3f14a42dfe6c",
        "documentMicroversion": "804bed6b532f04042b4cfc41",
        "documentId": "21f74f8fae0c4ccf061e2463"
      },
      {
        "name": "Part 1 <2>",
        "suppressed": false,
        "id": "MvW7NkK9OkQ8TI+lI",
        "type": "Part",
        "isStandardContent": false,
        "partId": "JHD",
        "fullConfiguration": "default",
        "configuration": "default",
        "elementId": "5c9bd028712a3f14a42dfe6c",
        "documentMicroversion": "804bed6b532f04042b4cfc41",
        "documentId": "21f74f8fae0c4ccf061e2463"
      }
    ],
    "patterns": [],
    "features": [],
    "fullConfiguration": "default",
    "configuration": "default",
    "elementId": "8b11049d66fbab779704ba8c",
    "documentMicroversion": "804bed6b532f04042b4cfc41",
    "documentId": "21f74f8fae0c4ccf061e2463"
  },
  "subAssemblies": [],
  "parts": [
    {
      "isStandardContent": false,
      "partId": "JHD",
      "bodyType": "solid",
      "fullConfiguration": "default",
      "configuration": "default",
      "elementId": "5c9bd028712a3f14a42dfe6c",
      "documentMicroversion": "804bed6b532f04042b4cfc41",
      "documentId": "21f74f8fae0c4ccf061e2463"
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
