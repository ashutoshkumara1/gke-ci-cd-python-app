pipeline {
    agent any
	//Create Environment for Google Cloud Project and GKE Cluster with Credentials
	environment {
		PROJECT_ID = 'optimistic-yeti-363002' //Project ID From Google Cloud Project
		CLUSTER_NAME = 'k8s-cluster' //Kubernetes Engine Cluster Name
		LOCATION = 'us-central1-c' //Kubernetes Engine Cluster Location
		CREDENTIALS_ID = 'kubernetes' //Credential Id Which Created in Jenkins for Kubernetes Credentials		
	}
	//Checking Github Connection and Pulling Github Application Repository.
    stages {
	    stage('Scm Checkout') {
		    steps {
		    	git branch: 'main', credentialsId: 'GIT_CREDENTIALS', url: 'https://github.com/ashutoshkumara1/gke-ci-cd-python-app.git'
			    //checkout scm
		    }
	    }
	    //removing the current running docker container
    	stage ('Stop previous running container'){
        	steps{
            	sh returnStatus: true, script: 'docker stop $(docker ps -a | grep ${JOB_NAME} | awk \'{print $1}\')'
            	sh returnStatus: true, script: 'docker rmi $(docker images | grep ${registry} | awk \'{print $3}\') --force' //this will delete all images
            	sh returnStatus: true, script: 'docker rm ${JOB_NAME}'
        	}
    	}
    	//Buliding Docker Image
	    stage('Build Docker Image') {
		    steps {
			    sh 'whoami'
			    script {
				    myimage = docker.build("ashutosha1/gcp-project:${env.BUILD_ID}")
			    }
		    }
	    }
	    //Pushing Docker Image to Docker Hub
	    stage("Push Docker Image") {
		    steps {
			    script {
				    echo "Push Docker Image"
				    withCredentials([string(credentialsId: 'DOCKER_HUB_CREDENTIALS', variable: 'DOCKER_HUB_CREDENTIALS')]) {
            				sh "docker login -u ashutosha1 -p ${DOCKER_HUB_CREDENTIALS}"
				    }
				        myimage.push("${env.BUILD_ID}")
				    
			    }
		    }
	    }
	    //Pulling Docker Imagr and Deploying Image to Kubernetes Cluster
	    stage('Deploy to K8s') {
		    steps{
			    echo "Deployment started ..."
			    sh 'ls -ltr'
			    sh 'pwd'
			    sh "sed -i 's/tagversion/${env.BUILD_ID}/g' serviceLB.yaml"
				sh "sed -i 's/tagversion/${env.BUILD_ID}/g' deployment.yaml"
			    echo "Start deployment of serviceLB.yaml"
			    step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'serviceLB.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
				echo "Start deployment of deployment.yaml"
				step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'deployment.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
			    echo "Deployment Finished ..."
			    script {
                    def stopcontainer = "docker stop ${JOB_NAME}"
                    def delcontName = "docker rm ${JOB_NAME}"
                    def delimages = 'docker image prune -a --force'
                    def drun = "docker run -d --name ${JOB_NAME} -p 5000:5000 ${img}"
                    println "${drun}"
                    }
		    }
	    }
    }
}
