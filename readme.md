
Rediseño de Sistema Distribuido (Cliente-Servidor)

 — El objetivo principal es transformar un sistema centralizado en una arquitectura distribuida utilizando sockets en Python y diseñando una infraestructura escalable. 
 
  Componentes del Sistema: El diseño del sistema está pensado para manejar alta disponibilidad y procesamiento en paralelo mediante los siguientes componentes:  
  
  Clientes: Aplicaciones móviles y web que envían peticiones mediante sockets TCP.  
  
  Balanceador de Carga (Nginx/HAProxy): Distribuye de forma equitativa el trafico entrante hacia los servidores disponibles. 
  
  Servidores Workers: Instancias independientes encargadas del procesamiento, optimizadas mediante un pool de hilos (Thread Pool). 
   
  Cola de Mensajes (RabbitMQ): Actúa como middleware para garantizar la comunicación asíncrona y el desacoplamiento entre servidores. 
    
  Almacenamiento Distribuido: Persistencia de datos lógicos en PostgreSQL y almacenamiento de archivos/objetos en Amazon S3.  
     
     Contenido:
     
    Esquema de la arquitectura de red y el flujo de datos en formato jpg.
      ENlace el Drawio: https://drive.google.com/file/d/1pUCZZz8Xti8LmAptZ4_ybfcT-mtiBSzf/view?usp=sharing
      
    /servidor: Código en Python que recibe las tareas por socket y administra los hilos de ejecución. 

    /cliente: Código en Python para la simulación de envío de tareas y recepción de resultados.