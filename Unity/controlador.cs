using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;

public class web : MonoBehaviour
{
    // ---------- Definición de struct ----------
    [System.Serializable]
    public struct Info {
        public Dictionary<string, int[]> posiciones;
        public Dictionary<string, int> calles;
        public Dictionary<string, int> paquetes;
    }

    [System.Serializable]
    public struct Paso {
        public Dictionary<int, Info> paso;
    }




    public Paso pasoCarro; // struct para poder manipular los datos
    public string uri; // URL del servidor


    // ---------- Request de servidor ----------

    [ContextMenu("Leer JSON")]
    public void LeerJSON(){
        StartCoroutine(CorrutinaLeerJSON());
    }

    IEnumerator CorrutinaLeerJSON(){
        UnityWebRequest server = UnityWebRequest.Get(uri);
        yield return server.SendWebRequest();

        // condición si vuelve el request
        if(!server.isNetworkError && !server.isHttpError){
            pasoCarro = JsonUtility.FromJson<Paso>(web.downloadHandler.text);

        } else {
            Debug.LogWarning("Hubo un problema con la lectura de los datos");
        } 
    }

