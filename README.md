```
----------   Table after insert   ----------


----------     Table metric     ----------
[id, code, description]
row 1:  (3, 'TB-001', 'Dog related')
row 2:  (4, 'TB-002', 'TV related')


----------     Table value_definition     ----------
[id, label, type, metric_id]
row 1:  (1, 'How many dogs do you own?', 'number', 3)
row 2:  (2, 'Favorite color of dog', 'text', 3)
row 3:  (3, 'Favorite show', 'text', 4)
row 4:  (4, 'Average hours per week spent watching tv', 'number', 4)
row 5:  (5, 'Favorite actor', 'text', 4)
```

```
{"message": "Novisto Demo"}

{"queryResult": "[(3, 'TB-001', 'Dog related'), (4, 'TB-002', 'TV related')]"}

{"metadata": 
    {
        "metric_code": ["TB-002","TB-002","TB-002"],
        "metric_description":["TV related","TV related","TV related"],
        "value_label":["Favorite show","Average hours per week spent watching tv","Favorite actor"],
        "value_type":["text","number","text"]
    }
}
```