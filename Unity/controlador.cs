using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

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

