package main

import (
  "net/http"
  "log"
  "github.com/gorilla/mux"
  "encoding/json"
  "math/rand"
  "fmt"
  "labix.org/v2/mgo"
  "labix.org/v2/mgo/bson"
)
var (
    session *mgo.Session
    collection *mgo.Collection
)

type Kitten struct {
    Id bson.ObjectId `bson:"_id" json:"id"`
    Name string `json:"name"`
    Picture string `json:"picture"`
}

type KittenJSON struct {
    Kitten Kitten `json:"kitten"`
}


type KittensJSON struct {
    Kittens []Kitten `json:"kittens"`
}


func CreateKittenHandler(w http.ResponseWriter, r *http.Request) {

    var kittenJSON KittenJSON

    err := json.NewDecoder(r.Body).Decode(&kittenJSON)
    if err != nil { panic(err) }

    kitten := kittenJSON.Kitten

    // Generate a random dimension for the kitten
    width := rand.Int() % 400
    height := rand.Int() % 400
    if width < 100 { width += 100 }
    if height < 100 { height += 100}
    kitten.Picture = fmt.Sprintf("http://placekitten.com/%d/%d", width, height)

    // Store the new kitten in the database
    // First, let's get a new id
    obj_id := bson.NewObjectId()
    kitten.Id = obj_id

    err = collection.Insert(&kitten)
    if err != nil { 
        panic(err)
    } else {
        log.Printf("Inserted new kitten %s with name %s", kitten.Id, kitten.Name)
    }

    j, err := json.Marshal(KittenJSON{Kitten: kitten})
    if err != nil { panic(err) }
    w.Header().Set("Content-Type", "application/json")
    w.Write(j)
}

func KittensHandler(w http.ResponseWriter, r *http.Request) {

    // Let's build up the kittens slice
    var mykittens []Kitten

    iter := collection.Find(nil).Iter()
    result := Kitten{}
    for iter.Next(&result) {
        mykittens = append(mykittens, result)
    }

    w.Header().Set("Content-Type", "application/json")
    j, err := json.Marshal(KittensJSON{Kittens: mykittens})
    if err != nil { panic (err) }
    w.Write(j)
    log.Println("Provided json")

}

func UpdateKittenHandler(w http.ResponseWriter, r *http.Request) {
    var err error
    // Grab the kitten's id from the incoming url
    vars := mux.Vars(r)
    id := bson.ObjectIdHex(vars["id"])

    // Decode the incoming kitten json
    var kittenJSON KittenJSON
    err = json.NewDecoder(r.Body).Decode(&kittenJSON)
    if err != nil {panic(err)}

    // Update the database
    err = collection.Update(bson.M{"_id":id},
             bson.M{"name":kittenJSON.Kitten.Name,
                    "_id": id,
                    "picture": kittenJSON.Kitten.Picture,
                    })
    if err == nil {
        log.Printf("Updated kitten %s name to %s", id, kittenJSON.Kitten.Name)
    } else { panic(err) }
    w.WriteHeader(http.StatusNoContent)
}

func DeleteKittenHandler(w http.ResponseWriter, r *http.Request) {
    // Grab the kitten's id from the incoming url
    var err error
    vars := mux.Vars(r)
    id := vars["id"]

    // Remove it from database
    err = collection.Remove(bson.M{"_id":bson.ObjectIdHex(id)})
    if err != nil { log.Printf("Could not find kitten %s to delete", id)}
    w.WriteHeader(http.StatusNoContent)
}
func main() {
    log.Println("Starting Server 2")

    r := mux.NewRouter()
    r.HandleFunc("/api/kittens", KittensHandler).Methods("GET")
    r.HandleFunc("/api/kittens", CreateKittenHandler).Methods("POST")
    r.HandleFunc("/api/kittens/{id}", UpdateKittenHandler).Methods("PUT")
    r.HandleFunc("/api/kittens/{id}", DeleteKittenHandler).Methods("DELETE")
    http.Handle("/api/", r)

    http.Handle("/", http.FileServer(http.Dir(".")))

    log.Println("Starting mongo db session")
    var err error
    session, err = mgo.Dial("localhost")
    if err != nil { panic (err) }
    defer session.Close()
    session.SetMode(mgo.Monotonic, true)
    collection = session.DB("Kittens").C("kittens")


    log.Println("Listening on 8080")
    http.ListenAndServe(":8080", nil)
}

