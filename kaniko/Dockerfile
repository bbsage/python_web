FROM busybox AS tools
# busybox 裡面有 sleep、cat、sh

FROM gcr.io/kaniko-project/executor:latest
COPY --from=tools /bin/sleep /bin/sleep
COPY --from=tools /bin/sh /bin/sh
COPY --from=tools /bin/cat /bin/cat
