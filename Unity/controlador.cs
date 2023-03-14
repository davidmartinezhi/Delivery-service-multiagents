using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;


// ------Clase que se obtendría del json-------
public class Frame {
    public Dictionary<int, Info> frame { get; set; }
}

public class Info {
    public Dictionary<string, int[]> posiciones { get; set; }
    public Dictionary<int[], int> calles { get; set; }
    public Dictionary<int[], int> paquetes { get; set; }
}




// ---- Request de servidor (aun falta de implemntar)-------
public class web : MonoBehaviour
{
    [ContextMenu("Leer simple")]
    public void LeerSimple(){
        StartCoroutine(CorrutinaLeerSimple());
    }

    IEnumerator CorrutinaLeerSimple(){
        UnityWebRequest server = UnityWebRequest.Get(uri)
        yield return server.SendWebRequest();

        // condición si vuelve el request
        if(!server.isNetworkError && !server.isHttpError){
            Debug.Log(server.downloadHandler.text);
        
        } else {
            Debug.LogWarning("hubo un problema")
        } 
    }   
}

