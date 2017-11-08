# Entitypedia
Entitypedia is an [Extended Named Entity](https://sites.google.com/site/extendednamedentity711/) Dictionary from Wikipedia.


## Getting started with the API
In this short tutorial, we introduce Entitypedia API.

### Request

```json
{
  "text": "東京",
  "type": "prefix"
}
```

### Response

```json
{
  "entities": [
    {
      "entity": "東京都",
      "type": "Location.GPE.Province",
      "uri": "http://ja.dbpedia.org/resource/東京都"
      }
    },
    {
      "entity": "東京テレポート駅",
      "type": "Facility.Line.Station",
      "uri": "http://ja.dbpedia.org/resource/東京テレポート駅"
      }
    },
  ...
  ]
}
```

Entities would be sorted by their importance.