{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "complex-k8s.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "complex-k8s.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "complex-k8s.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "complex-k8s.labels" -}}
app.kubernetes.io/name: {{ include "complex-k8s.name" . }}
helm.sh/chart: {{ include "complex-k8s.chart" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "complex-k8s.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "complex-k8s.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{- define "complex-k8s.specRulesHttpPaths" }}
{{- $fullName := include "complex-k8s.fullname" . -}}
{{- range $k,$v := .Values.ingress.expose }}
- path: {{ $v.path }}
  backend:
{{ if eq $k "kibana" }}
    serviceName: {{ printf "%s-%s"  $.Release.Name  $k }}
    servicePort: {{ $v.clusterPort }}
{{ else }}
    serviceName: {{ printf "%s-%s-cluster-ip-service"  $fullName  $k }}
    servicePort: {{ $v.clusterPort }}
{{ end }}
{{- end -}}
{{- end -}}
