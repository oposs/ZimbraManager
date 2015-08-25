#!/bin/bash

. `dirname $0`/sdbs.inc

# iam-mailserver-interface
for module in \
  XML::Compile::WSDL11@3.03 \
  XML::Compile::SOAP11@3.10 \
  XML::Compile::Transport::SOAPHTTP@3.10 \
  Net::HTTP@6.09 \
  Mojolicious@6.17 \
  LWP::Protocol::https@6.06 \
  IO::Socket::SSL@2.017 \
  HTTP::CookieJar@0.007 \
; do
  perlmodule $module
done
